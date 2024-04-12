from flask import Flask, render_template
from dotenv import load_dotenv
import os

from models import db, FinancialData, Article
from api_calls import fetch_exchange_rate
from scrape1 import scrape_content, save_article, urls

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

@app.route('/fetch-rate')
def fetch_and_store_rate():
    try:
        rate = fetch_exchange_rate()
        if rate:
            new_rate = FinancialData(currency_pair="USD/CAD", rate=float(rate), date_fetched=datetime.utcnow())
            db.session.add(new_rate)
            db.session.commit()
            return f"Stored new rate: {rate}"
        else:
            return "No rate received from fetch function"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/scrape-articles')
def scrape_and_store_articles():
    try:
        for url in urls:
            title, content = scrape_content(url)
            if title and content:
                save_article(url, title, content)
        return "Articles scraped and stored successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
@app.route('/')
def index():
    rates = FinancialData.query.order_by(FinancialData.date_fetched.desc()).all()
    return render_template('index.html', rates=rates)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
