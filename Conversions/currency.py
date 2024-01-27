import tkinter as tk
import requests
import json
import os
from datetime import datetime
from utils.utils import validate_number, clear_window, main_menu

URL_API = "https://api.exchangerate-api.com/v4/latest/USD"
FILE_NAME = "exchange_rates.json"

def currency_conversion(window):
    clear_window(window)
    for i in range(6):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    rates = fetch_currencies(URL_API, FILE_NAME)

    if rates is None:
        tk.Label(window, text="Unable to fetch new data and no local data available.").grid(row=0, column=0, sticky="nsew")
        return

    currencies = list(rates['rates'].keys())

    tk.Label(window, text="Select your source currency:").grid(row=1, column=0, sticky="nsew")
    source_currency_var = tk.StringVar(window)
    source_currency_menu = tk.OptionMenu(window, source_currency_var, *currencies)
    source_currency_menu.grid(row=2, column=0, sticky="nsew")

    tk.Label(window, text="Select the target currency:").grid(row=3, column=0, sticky="nsew")
    target_currency_var = tk.StringVar(window)
    target_currency_menu = tk.OptionMenu(window, target_currency_var, *currencies)
    target_currency_menu.grid(row=4, column=0, sticky="nsew")

    tk.Label(window, text="Enter the amount to be converted:").grid(row=5, column=0, sticky="nsew")
    amount_entry = tk.Entry(window)
    amount_entry.grid(row=6, column=0, sticky="ew")

    convert_button = tk.Button(window, text="Convert", command=lambda: perform_currency_conversion(window, rates, source_currency_var.get(), target_currency_var.get(), amount_entry.get()))
    convert_button.grid(row=7, column=0, sticky="nsew")

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=8, column=0, sticky="nsew")


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
    # Konfiguracja wagi wierszy i kolumn dla responsywności
    for i in range(5):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    amount = validate_number(amount_str, window, lambda: currency_conversion(window))
    if amount is None:
        return

    if source_currency in rates['rates'] and target_currency in rates['rates']:
        conversion_factor = rates['rates'][target_currency] / rates['rates'][source_currency]
        result = amount * conversion_factor
        fetch_date_label = tk.Label(window, text=f"The data is from this date: {rates['fetch_date']}")
        fetch_date_label.grid(row=0, column=0, sticky="ew")
        result_label = tk.Label(window, text=f"{amount} {source_currency} = {result:.2f} {target_currency}")
        result_label.grid(row=1, column=0, sticky="ew")
    else:
        unknown_currency_label = tk.Label(window, text="Unknown currency.")
        unknown_currency_label.grid(row=0, column=0, sticky="ew")

    new_conversion_button = tk.Button(window, text="New Conversion", command=lambda: currency_conversion(window))
    new_conversion_button.grid(row=2, column=0, sticky="ew")

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=3, column=0, sticky="ew")
