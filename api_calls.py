import requests

response = requests.get('https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=5')
usd_cad_data = response.json()
print(usd_cad_data)


import requests

def fetch_exchange_rate():
    try: 
        response = requests.get('https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?recent=5')
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "Failed to fetch data", response.status_code
    except requests.RequestException as e:
        return str(e)
