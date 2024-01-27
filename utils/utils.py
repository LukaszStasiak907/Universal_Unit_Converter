import tkinter as tk
import json
import os

def validate_number(input_str, window, back_function):
    try:
        return float(input_str)
    except ValueError:
        tk.Label(window, text="This is not a valid number.").grid(row=0, column=0, sticky="w")
        tk.Button(window, text="Back", command=back_function).grid(row=1, column=0, sticky="ew")
        return None

def load_conversion_factors(conversion_type):
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    with open(json_file, 'r') as file:
        conversion_factors = json.load(file)
    return conversion_factors

def add_new_unit(window):
    clear_window(window)
    for i in range(8):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    tk.Label(window, text="Enter the name of the new unit (e.g., 'My Unit'):").grid(row=0, column=0, sticky="w")
    source_unit_entry = tk.Entry(window)
    source_unit_entry.grid(row=1, column=0, sticky="ew")

    tk.Label(window, text="Enter the target unit this corresponds to (e.g., 'meter'):").grid(row=2, column=0, sticky="w")
    target_unit_entry = tk.Entry(window)
    target_unit_entry.grid(row=3, column=0, sticky="ew")

    tk.Label(window, text="Enter how many target units make one source unit:").grid(row=4, column=0, sticky="w")
    multiplier_entry = tk.Entry(window)
    multiplier_entry.grid(row=5, column=0, sticky="ew")

    add_button = tk.Button(window, text="Add Unit", command=lambda: perform_add_new_unit(window, source_unit_entry.get(), target_unit_entry.get(), multiplier_entry.get()))
    add_button.grid(row=6, column=0, sticky="ew")

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=7, column=0, sticky="ew")

def perform_add_new_unit(window, source_unit, target_unit, multiplier_str):
    multiplier = validate_number(multiplier_str, window, lambda: add_new_unit(window))
    if multiplier is None or multiplier == 0:
        return

    converter_custom = 'Unit_Converters/converter_custom.json'
    try:
        with open(converter_custom, 'r') as file:
            custom_units = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        custom_units = {}

    forward_key = f"{source_unit.upper()}_{target_unit.upper()}"
    custom_units[forward_key] = {"multiplier": multiplier}

    backward_key = f"{target_unit.upper()}_{source_unit.upper()}"
    custom_units[backward_key] = {"multiplier": 1 / multiplier}

    with open(converter_custom, 'w') as file:
        json.dump(custom_units, file, indent=4)

    tk.Label(window, text=f"Units {source_unit.upper()} <=> {target_unit.upper()} have been added.").grid(row=8, column=0, sticky="w")
    new_unit_button = tk.Button(window, text="Add Another Unit", command=lambda: add_new_unit(window))
    new_unit_button.grid(row=9, column=0, sticky="ew")

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=10, column=0, sticky="ew")

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def create_dropdown_menu(window, label_text, options, row):
    label = tk.Label(window, text=label_text)
    label.grid(row=row, column=0, sticky="w")
    var = tk.StringVar(window)
    var.set(options[0])  # ustawienie domyślnej wartości
    menu = tk.OptionMenu(window, var, *options)
    menu.grid(row=row+1, column=0, sticky="ew")
    return var


def main_menu(window):
    clear_window(window)
    import main  # Import inside the function to avoid circular dependency
    main.main_menu(window)
