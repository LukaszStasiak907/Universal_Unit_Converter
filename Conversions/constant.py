import tkinter as tk
import os
import json
from utils.utils import validate_number, clear_window, main_menu, create_dropdown_menu


def get_conversion_types():
    """Retrieves a list of available conversion types from the 'Unit_Converters' directory.

    Returns:
    list: A list of strings representing the different types of conversions available.
    """
    directory = "Unit_Converters"
    conversion_files = os.listdir(directory)
    conversion_types = [file.replace("converter_", "").replace(".json", "") for file in conversion_files if
                        file.startswith("converter_") and file.endswith(".json")]
    return conversion_types


def choose_conversion(window):
    """Sets up the GUI for choosing a conversion type.

    Parameters:
    window (tk.Tk): The tkinter window where the GUI components will be added.

    This function allows the user to select a conversion type from a dropdown menu and proceed to the conversion screen.
    """
    clear_window(window)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    conversion_types = get_conversion_types()
    conversion_type_var = create_dropdown_menu(window, "Select the conversion type:", conversion_types, 0, 1)

    submit_button = tk.Button(window, text="Select", command=lambda: conversion_screen(window, conversion_type_var.get()))
    submit_button.grid(row=2, column=0, sticky="ew")
    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=3, column=0, sticky="ew")


def conversion_screen(window, conversion_type):
    """Sets up the GUI for performing a unit conversion of a specified type.

    Parameters:
    window (tk.Tk): The tkinter window where the GUI components will be added.
    conversion_type (str): The type of conversion to perform.

    This function displays options for source and target units and an entry field for the value to be converted.
    """
    clear_window(window)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    try:
        with open(json_file, 'r') as file:
            units_data = json.load(file)
    except FileNotFoundError:
        tk.Label(window, text=f"No conversion file found for '{conversion_type}'.").grid(row=0, column=0, sticky="nsew")
        return

    units = set()
    for unit_pair in units_data.keys():
        units.update(unit_pair.split("_"))

    source_unit_var = create_dropdown_menu(window, "Select source unit:", list(units), 2, 3)
    target_unit_var = create_dropdown_menu(window, "Select target unit:", list(units), 4, 5)

    tk.Label(window, text="Enter the value to be converted:").grid(row=6, column=0, sticky="nsew")
    value_entry = tk.Entry(window)
    value_entry.grid(row=7, column=0, sticky="ew")

    convert_button = tk.Button(window, text="Convert",
                               command=lambda: perform_conversion(window, value_entry.get(), source_unit_var.get(),
                                                                  target_unit_var.get(), conversion_type))
    convert_button.grid(row=8, column=0, sticky="ew")
    tk.Button(window, text="Back", command=lambda: choose_conversion(window)).grid(row=9, column=0, sticky="ew")


def perform_conversion(window, value_str, source_unit, target_unit, conversion_type):
    """
    Performs the unit conversion and displays the result.

    Parameters:
    window (tk.Tk): The tkinter window where the results will be displayed.
    value_str (str): The string representation of the value to be converted.
    source_unit (str): The unit of the input value.
    target_unit (str): The unit into which the value is to be converted.
    conversion_type (str): The type of conversion to perform.

    This function validates the input value, performs the conversion, and displays the result or an error message.
    """
    clear_window(window)
    for i in range(4):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    value = validate_number(value_str, window, lambda: conversion_screen(window, conversion_type))
    if value is None:
        return

    outcome = calculate(value, source_unit, target_unit, conversion_type)
    if outcome is not None:
        result_label = tk.Label(window, text=f"{value} {source_unit} = {outcome:.2f} {target_unit}")
        result_label.grid(row=0, column=0, sticky="ew")
    else:
        error_label = tk.Label(window, text="Conversion failed. Check your units.")
        error_label.grid(row=0, column=0, sticky="ew")

    new_conversion_button = tk.Button(window, text="New Conversion", command=lambda: choose_conversion(window))
    new_conversion_button.grid(row=1, column=0, sticky="ew")
    main_menu_button = tk.Button(window, text="Main Menu", command=lambda: main_menu(window))
    main_menu_button.grid(row=2, column=0, sticky="ew")


def calculate(value, source_unit, target_unit, conversion_type):
    """Calculates the converted value based on the specified units and conversion type.

    Parameters:
    value (float): The value to be converted.
    source_unit (str): The unit of the input value.
    target_unit (str): The unit into which the value is to be converted.
    conversion_type (str): The type of conversion to perform.

    Returns:
    float: The converted value.

    This function handles both predefined and custom conversion factors.
    """
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
        if source_unit in conversion_factors:
            value *= conversion_factors[source_unit]["multiplier"]
        if target_unit in conversion_factors:
            value /= conversion_factors[target_unit]["multiplier"]

    return value


def load_conversion_factors(conversion_type):
    """Loads conversion factors from a JSON file based on the specified conversion type.

    Parameters:
    conversion_type (str): The type of conversion (e.g., 'length', 'weight') for which the factors are required.

    Returns:
    dict: A dictionary containing the conversion factors for the specified type.
    """
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    with open(json_file, 'r') as file:
        conversion_factors = json.load(file)
    return conversion_factors
