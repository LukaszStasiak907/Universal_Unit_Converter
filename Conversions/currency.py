import tkinter as tk
import requests
import json
import os
from datetime import datetime
from utils.utils import validate_number, clear_window, main_menu, create_dropdown_menu

URL_API = "https://api.exchangerate-api.com/v4/latest/USD"
FILE_NAME = "exchange_rates.json"


def currency_conversion(window):
    clear_window(window)
    rates = fetch_currencies(URL_API, FILE_NAME)

    if rates is None:
        tk.Label(window, text="Unable to fetch new data and no local data available.").pack()
        return

    currencies = list(rates['rates'].keys())

    source_currency_var = create_dropdown_menu(window, "Select your source currency:", currencies)
    target_currency_var = create_dropdown_menu(window, "Select the target currency:", currencies)

    tk.Label(window, text="Enter the amount to be converted:").pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack()

    convert_button = tk.Button(window, text="Convert",
                               command=lambda: perform_currency_conversion(window, rates, source_currency_var.get(),
                                                                           target_currency_var.get(),
                                                                           amount_entry.get()))
    convert_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.pack()


def fetch_currencies(url_api, file_name):
    selected_currencies = ["USD", "EUR", "CHF", "GBP", "CNY", "JPY", "PLN", "CZK"]
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        data = response.json()

        filtered_rates = {currency: data['rates'].get(currency) for currency in selected_currencies}

        selected_data = {
            'fetch_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'base': data.get('base'),
            'rates': filtered_rates
        }

        with open(file_name, 'w') as f:
            json.dump(selected_data, f)
        return selected_data

    except requests.RequestException as e:
        print(f"Error during downloading currency rates: {e}")
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return json.load(f)
        return None


def perform_currency_conversion(window, rates, source_currency, target_currency, amount_str):
    clear_window(window)
    amount = validate_number(amount_str, window, lambda: currency_conversion(window))
    if amount is None:
        return

    if source_currency in rates['rates'] and target_currency in rates['rates']:
        conversion_factor = rates['rates'][target_currency] / rates['rates'][source_currency]
        result = amount * conversion_factor
        tk.Label(window, text=f"The data is from this date: {rates['fetch_date']}").pack()
        tk.Label(window, text=f"{amount} {source_currency} = {result:.2f} {target_currency}").pack()
    else:
        tk.Label(window, text="Unknown currency.").pack()

    new_conversion_button = tk.Button(window, text="New Conversion", command=lambda: currency_conversion(window))
    new_conversion_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.pack()