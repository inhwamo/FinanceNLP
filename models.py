from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_pair = db.Column(db.String(10), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    date_fetched = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Rate {self.currency_pair} - {self.rate}>"
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(1024), unique=True, nullable=False)
    date_scraped = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.title}>"
