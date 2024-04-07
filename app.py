import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)


# Use DATABASE_URL from the environment variables in production (Heroku)
# Fall back to SQLite for local development

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db').replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(app)

class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_pair = db.Column(db.String(10), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    date_fetched = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Rate {self.currency_pair} - {self.rate}>"

def fetch_exchange_rate():
    url = "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=5"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Adjusted according to the actual API response structure
        latest_rate = data['observations'][-1]['FXUSDCAD']['v']
        return latest_rate
    else:
        print("Failed to fetch data")
        return None

@app.route('/fetch-rate')
def fetch_and_store_rate():
    rate = fetch_exchange_rate()
    if rate:
        new_rate = FinancialData(currency_pair="USD/CAD", rate=float(rate))
        db.session.add(new_rate)
        db.session.commit()
        return f"Stored new rate: {rate}"
    return "Failed to fetch and store rate"

@app.route('/')
def index():
    # Display the latest rates
    rates = FinancialData.query.order_by(FinancialData.date_fetched.desc()).all()
    return render_template('index.html', rates=rates)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


