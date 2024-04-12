import requests
from datetime import datetime
from app import db, FinancialData  # Ensure these are imported correctly

def fetch_exchange_rate():
    try:
        response = requests.get('https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=5')
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])
            for observation in observations:
                rate = observation.get('FXUSDCAD', {}).get('v')
                if rate:
                    date_str = observation.get('d')  # Assuming 'd' is the date key
                    rate_date = datetime.strptime(date_str, '%Y-%m-%d')
                    # Check if this date already exists in the database
                    existing_rate = FinancialData.query.filter_by(date_fetched=rate_date).first()
                    if not existing_rate:
                        new_rate = FinancialData(currency_pair="USD/CAD", rate=float(rate), date_fetched=rate_date)
                        db.session.add(new_rate)
            db.session.commit()
            return "Data fetched and stored successfully."
        else:
            return "Failed to fetch data", response.status_code
    except requests.RequestException as e:
        return str(e)
