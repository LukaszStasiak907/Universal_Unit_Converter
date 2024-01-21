import os
import requests
import json
from datetime import datetime
from utils import utils

URL_API = "https://api.exchangerate-api.com/v4/latest/USD"
FILE_NAME = "exchange_rates.json"


def fetch_currencies(url_api, file_name):
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        data = response.json()
        selected_data = {
            'fetch_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'base': data.get('base'),
            'rates': data.get('rates')
        }

        with open(file_name, 'w') as f:
            json.dump(selected_data, f)
        print("Currency rates downloaded and saved.")

    except requests.RequestException as e:
        print(f"Error during downloading currency rates: {e}")


def currency_conversion():
    if not os.path.exists(FILE_NAME):
        print("No local exchange rate data. Downloading...")
        fetch_currencies(URL_API, FILE_NAME)

    with open(FILE_NAME, 'r') as f:
        rates = json.load(f)

    source_currency = input("Enter your source currency (e.g. USD): ").upper()
    target_currency = input("Enter the target currency (e.g. EUR): ").upper()
    amount = utils.validate_number(input("Enter the amount to be converted: "))

    if amount is None:
        return

    if source_currency in rates['rates'] and target_currency in rates['rates']:
        conversion_factor = rates['rates'][target_currency] / rates['rates'][source_currency]
        result = amount * conversion_factor
        print(f"The data is from this date: {rates['fetch_date']}")
        print(f"{amount} {source_currency} = {result:.2f} {target_currency}")
    else:
        print("Unknown currency.")
