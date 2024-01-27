import tkinter as tk
from tkinter import ttk
from utils import load_conversion_factors, validate_number

def calculate_constant(value, source_unit, target_unit, conversion_factors):
    source_unit = source_unit.upper()
    target_unit = target_unit.upper()

    if source_unit == target_unit:
        return value

    # Konwersja dla niestandardowych jednostek
    custom_key = f"{source_unit}_{target_unit}"
    if custom_key in conversion_factors:
        return value * conversion_factors[custom_key]["multiplier"]

    # Konwersja dla standardowych jednostek
    if source_unit in conversion_factors and target_unit in conversion_factors:
        # Przeliczanie na jednostkę bazową, jeśli to nie jednostka bazowa
        if source_unit != 'BASE':
            value *= conversion_factors[source_unit]["multiplier"]

        # Przeliczanie z jednostki bazowej na docelową
        if target_unit != 'BASE':
            value /= conversion_factors[target_unit]["multiplier"]

        return value

    return None

def get_constant_frame(root, conversion_type):
    frame = ttk.Frame(root)

    # Pobranie dostępnych jednostek dla danego typu konwersji
    units = load_conversion_factors(conversion_type).keys()

    # Tworzenie widgetów
    ttk.Label(frame, text="Wartość do konwersji:").pack()
    value_entry = ttk.Entry(frame)
    value_entry.pack()

    ttk.Label(frame, text="Jednostka źródłowa:").pack()
    source_unit_combobox = ttk.Combobox(frame, values=units)
    source_unit_combobox.pack()

    ttk.Label(frame, text="Jednostka docelowa:").pack()
    target_unit_combobox = ttk.Combobox(frame, values=units)
    target_unit_combobox.pack()

    result_label = ttk.Label(frame)
    result_label.pack()

    def on_calculate():
        try:
            value = validate_number(value_entry.get())
            source_unit = source_unit_combobox.get()
            target_unit = target_unit_combobox.get()

            conversion_factors = load_conversion_factors(conversion_type)
            result = calculate_constant(value, source_unit, target_unit, conversion_factors)
            if result is not None:
                result_label.config(text=f"Wynik: {result:.2f}")
            else:
                result_label.config(text="Nie można przeprowadzić konwersji.")
        except Exception as e:
            result_label.config(text=f"Błąd: {str(e)}")

    ttk.Button(frame, text="Oblicz", command=on_calculate).pack()

    return frame
