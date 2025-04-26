import os
import requests
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
# BASE_URL = 'https://v6.exchangerate-api.com/v6/6061aa18da46726564c24452/latest/USD'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest'

def get_exchange_rate(base_currency: str, target_currency: str):
    url = f"{BASE_URL}/{base_currency.upper()}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return data["conversion_rates"][target_currency.upper()]