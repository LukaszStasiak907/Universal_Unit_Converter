import tkinter as tk
import os
import json
from utils.utils import validate_number, clear_window, main_menu, create_dropdown_menu


def get_conversion_types():
    directory = "Unit_Converters"
    conversion_files = os.listdir(directory)
    conversion_types = [file.replace("converter_", "").replace(".json", "") for file in conversion_files if
                        file.startswith("converter_") and file.endswith(".json")]
    return conversion_types


def choose_conversion(window):
    clear_window(window)

    conversion_types = get_conversion_types()
    conversion_type_var = create_dropdown_menu(window, "Select the conversion type:", conversion_types)

    tk.Button(window, text="Submit", command=lambda: conversion_screen(window, conversion_type_var.get())).pack()
    tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window)).pack()


def conversion_screen(window, conversion_type):
    clear_window(window)

    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    try:
        with open(json_file, 'r') as file:
            units_data = json.load(file)
    except FileNotFoundError:
        tk.Label(window, text=f"No conversion file found for '{conversion_type}'.").pack()
        return

    units = set()
    for unit_pair in units_data.keys():
        units.update(unit_pair.split("_"))

    source_unit_var = create_dropdown_menu(window, "Select source unit:", list(units))
    target_unit_var = create_dropdown_menu(window, "Select target unit:", list(units))

    tk.Label(window, text="Enter the value to be converted:").pack()
    value_entry = tk.Entry(window)
    value_entry.pack()

    convert_button = tk.Button(window, text="Convert",
                               command=lambda: perform_conversion(window, value_entry.get(), source_unit_var.get(),
                                                                  target_unit_var.get(), conversion_type))
    convert_button.pack()
    tk.Button(window, text="Back", command=lambda: choose_conversion(window)).pack()


def perform_conversion(window, value_str, source_unit, target_unit, conversion_type):
    clear_window(window)
    value = validate_number(value_str, window, lambda: conversion_screen(window, conversion_type))
    if value is None:
        return

    outcome = calculate(value, source_unit, target_unit, conversion_type)
    if outcome is not None:
        tk.Label(window, text=f"{value} {source_unit} to {outcome:.2f} {target_unit}").pack()
    else:
        tk.Label(window, text="Conversion failed. Check your units.").pack()

    tk.Button(window, text="New Conversion", command=lambda: choose_conversion(window)).pack()
    tk.Button(window, text="Main Menu", command=lambda: main_menu(window)).pack()


def calculate(value, source_unit, target_unit, conversion_type):
    conversion_factors = load_conversion_factors(conversion_type)
    custom_conversion_factors = load_conversion_factors("custom")
    source_unit = source_unit.upper()
    target_unit = target_unit.upper()

    custom_key = f"{source_unit}_{target_unit}"

    if custom_key in custom_conversion_factors:
        value *= custom_conversion_factors[custom_key]["multiplier"]
    elif conversion_type == "temperature":
        if source_unit != "K":
            key = f"{source_unit}_K"
            if key in conversion_factors:
                factor = conversion_factors[key]
                value = (value + factor["offset"]) * factor["multiplier"]
                if "to_kelvin_offset" in factor:
                    value += factor["to_kelvin_offset"]
            else:
                print(f"No conversion rate for: {source_unit} to K")
                return None

        if target_unit != "K":
            key = f"K_{target_unit}"
            if key in conversion_factors:
                factor = conversion_factors[key]
                value = value * factor["multiplier"] + factor["offset"]
            else:
                print(f"No conversion rate for: K to {target_unit}")
                return None
    else:
        if source_unit != 'KG' and source_unit in conversion_factors:
            value *= conversion_factors[source_unit]["multiplier"]
        if target_unit != 'KG' and target_unit in conversion_factors:
            value /= conversion_factors[target_unit]["multiplier"]

    return value


def load_conversion_factors(conversion_type):
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    with open(json_file, 'r') as file:
        conversion_factors = json.load(file)
    return conversion_factors
