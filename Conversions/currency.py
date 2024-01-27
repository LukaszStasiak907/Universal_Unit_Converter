import tkinter as tk
from tkinter import ttk
import requests
import json
from utils import validate_number

# Adres URL API do pobierania kursów walut
URL_API = "https://api.exchangerate-api.com/v4/latest/USD"
FILE_NAME = "exchange_rates.json"

def fetch_currencies():
    try:
        response = requests.get(URL_API)
        response.raise_for_status()
        data = response.json()
        with open(FILE_NAME, 'w') as f:
            json.dump(data, f)
        return data['rates']
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania kursów walut: {e}")
        try:
            with open(FILE_NAME, 'r') as f:
                return json.load(f)['rates']
        except (FileNotFoundError, json.JSONDecodeError):
            return None

def calculate_currency(amount, source_currency, target_currency, rates):
    if source_currency in rates and target_currency in rates:
        conversion_factor = rates[target_currency] / rates[source_currency]
        return amount * conversion_factor
    return None

def get_currency_frame(root):
    frame = ttk.Frame(root)

    # Pobranie aktualnych kursów walut
    rates = fetch_currencies()
    if not rates:
        ttk.Label(frame, text="Błąd: Nie udało się pobrać kursów walut.").pack()
        return frame

    currencies = list(rates.keys())

    # Tworzenie widgetów
    ttk.Label(frame, text="Kwota:").pack()
    amount_entry = ttk.Entry(frame)
    amount_entry.pack()

    ttk.Label(frame, text="Waluta źródłowa:").pack()
    source_currency_combobox = ttk.Combobox(frame, values=currencies)
    source_currency_combobox.pack()

    ttk.Label(frame, text="Waluta docelowa:").pack()
    target_currency_combobox = ttk.Combobox(frame, values=currencies)
    target_currency_combobox.pack()

    result_label = ttk.Label(frame)
    result_label.pack()

    def on_calculate():
        try:
            amount = validate_number(amount_entry.get())
            source_currency = source_currency_combobox.get()
            target_currency = target_currency_combobox.get()

            result = calculate_currency(amount, source_currency, target_currency, rates)
            if result is not None:
                result_label.config(text=f"Wynik: {result:.2f} {target_currency}")
            else:
                result_label.config(text="Nie można przeprowadzić konwersji.")
        except Exception as e:
            result_label.config(text=f"Błąd: {str(e)}")

    ttk.Button(frame, text="Oblicz", command=on_calculate).pack()

    return frame
