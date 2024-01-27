import tkinter as tk
from utils import utils
import json

def calculate(value, source_unit, target_unit, conversion_type):
    conversion_factors = utils.load_conversion_factors(conversion_type)
    custom_conversion_factors = utils.load_conversion_factors("custom")
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


def choose_conversion(window):
    clear_window(window)

    tk.Label(window, text="Enter the conversion type (e.g. 'length', 'temperature'):").pack()
    conversion_type_entry = tk.Entry(window)
    conversion_type_entry.pack()

    tk.Button(window, text="Submit",
              command=lambda: conversion_screen(window, conversion_type_entry.get().lower())).pack()
    tk.Button(window, text="Back to Main Menu", command=lambda: utils.main_menu(window)).pack()


def conversion_screen(window, conversion_type):
    clear_window(window)

    json_file = f'Unit_Converters/converter_{conversion_type}.json'

    try:
        with open(json_file, 'r') as file:
            units = json.load(file).keys()
    except FileNotFoundError:
        tk.Label(window, text=f"No conversion file found for '{conversion_type}'.").pack()
        return

    if conversion_type == "temperature":
        display_units = {"C", "K", "F"}
    else:
        display_units = set()
        for key in units:
            display_units.update(key.split("_"))

    tk.Label(window, text="Available units: " + ", ".join(sorted(display_units))).pack()

    tk.Label(window, text="Enter source unit:").pack()
    source_unit_entry = tk.Entry(window)
    source_unit_entry.pack()

    tk.Label(window, text="Enter target unit:").pack()
    target_unit_entry = tk.Entry(window)
    target_unit_entry.pack()

    tk.Label(window, text="Enter the value to be converted:").pack()
    value_entry = tk.Entry(window)
    value_entry.pack()

    tk.Button(window, text="Convert",
              command=lambda: perform_conversion(window, value_entry.get(), source_unit_entry.get(),
                                                 target_unit_entry.get(), conversion_type)).pack()
    tk.Button(window, text="Back", command=lambda: choose_conversion(window)).pack()


def perform_conversion(window, value, source_unit, target_unit, conversion_type):
    clear_window(window)
    try:
        value = float(value)
    except ValueError:
        tk.Label(window, text="This is not a valid number.").pack()
        return

    outcome = calculate(value, source_unit, target_unit, conversion_type)
    if outcome is not None:
        tk.Label(window, text=f"{value} {source_unit} to {outcome:.2f} {target_unit}").pack()
    else:
        tk.Label(window, text="Conversion failed. Check your units.").pack()

    tk.Button(window, text="New Conversion", command=lambda: choose_conversion(window)).pack()
    tk.Button(window, text="Main Menu", command=lambda: utils.main_menu(window)).pack()


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
