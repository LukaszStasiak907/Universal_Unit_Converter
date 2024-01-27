from utils import utils
import json


def calculate(value, source_unit, target_unit, conversion_type):
    conversion_factors = utils.load_conversion_factors(conversion_type)
    source_unit = source_unit.upper()
    target_unit = target_unit.upper()

    if conversion_type != "temperature":
        # Konwersja na jednostkę bazową
        if source_unit in conversion_factors:
            value /= conversion_factors[source_unit]["multiplier"]
        else:
            print(f"No conversion rate from {source_unit} to base unit.")
            return None

        # Konwersja z jednostki bazowej na docelową
        if target_unit in conversion_factors:
            value *= conversion_factors[target_unit]["multiplier"]
        else:
            print(f"No conversion rate from base unit to {target_unit}.")
            return None
    else:
        # Dla temperatury użyj istniejącego systemu
        key = f"{source_unit}_{target_unit}"
        if key in conversion_factors:
            conversion_factor = conversion_factors[key]
            value += conversion_factor.get("pre_offset", 0)
            value *= conversion_factor.get("multiplier", 1)
            value += conversion_factor.get("post_offset", 0)
        else:
            print(f"No conversion rate for: {source_unit} to {target_unit}")
            return None

    return value




def choose_conversion():
    conversion_type = input("Enter the conversion type (e.g. 'length', 'temperature'): ").lower()
    json_file = f'Unit_Converters/converter_{conversion_type}.json'

    try:
        with open(json_file, 'r') as file:
            units = json.load(file).keys()
    except FileNotFoundError:
        print(f"No conversion file found for '{conversion_type}'.")
        return

    print("Available units:", ", ".join(units))
    source_unit = input("Enter source unit: ").lower()
    target_unit = input("Enter target unit: ").lower()

    value = utils.validate_number(input("Enter the value to be converted: "))

    if source_unit == target_unit:
        print(f"{value} {source_unit} to {value:.2f} {target_unit}")
        return

    if value is None:
        return

    outcome = calculate(value, source_unit, target_unit, conversion_type)
    print(f"{value} {source_unit} to {outcome:.2f} {target_unit}")
