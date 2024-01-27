import tkinter as tk
import json

def validate_number(input_str):
    try:
        return float(input_str)
    except ValueError:
        return None

def load_conversion_factors(conversion_type):
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    with open(json_file, 'r') as file:
        conversion_factors = json.load(file)
    return conversion_factors

def add_new_unit(window):
    clear_window(window)
    tk.Label(window, text="Enter the name of the new unit (e.g., 'My Unit'):").pack()
    source_unit_entry = tk.Entry(window)
    source_unit_entry.pack()

    tk.Label(window, text="Enter the target unit this corresponds to (e.g., 'meter'):").pack()
    target_unit_entry = tk.Entry(window)
    target_unit_entry.pack()

    tk.Label(window, text="Enter how many target units make one source unit:").pack()
    multiplier_entry = tk.Entry(window)
    multiplier_entry.pack()

    add_button = tk.Button(window, text="Add Unit", command=lambda: perform_add_new_unit(window, source_unit_entry.get(), target_unit_entry.get(), multiplier_entry.get()))
    add_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.pack()

def perform_add_new_unit(window, source_unit, target_unit, multiplier_str):
    multiplier = validate_number(multiplier_str)
    if multiplier is None or multiplier == 0:
        tk.Label(window, text="Invalid multiplier. The new unit was not added.").pack()
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

    tk.Label(window, text=f"Units {source_unit.upper()} <=> {target_unit.upper()} have been added.").pack()
    new_unit_button = tk.Button(window, text="Add Another Unit", command=lambda: add_new_unit(window))
    new_unit_button.pack()

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.pack()

def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

def main_menu(window):
    clear_window(window)
    import main  # Import inside the function to avoid circular dependency
    main.main_menu(window)
