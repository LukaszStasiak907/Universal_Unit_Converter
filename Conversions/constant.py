from utils import utils
import json

def calculate(value, source_unit, target_unit, conversion_type):
    conversion_factors = utils.load_conversion_factors(conversion_type)
    source_unit = source_unit.upper()
    target_unit = target_unit.upper()

    if conversion_type == "temperature":
        # Konwersja na Kelwiny, jeśli potrzebna
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

        # Konwersja z Kelwinów na jednostkę docelową
        if target_unit != "K":
            key = f"K_{target_unit}"
            if key in conversion_factors:
                factor = conversion_factors[key]
                value = value * factor["multiplier"] + factor["offset"]
            else:
                print(f"No conversion rate for: K to {target_unit}")
                return None
    else:
        # Dla innych typów konwersji (np. długość, ciężar)
        # Przeliczanie na jednostkę bazową, jeśli to nie jednostka bazowa
        if source_unit != 'KG' and source_unit in conversion_factors:
            value *= conversion_factors[source_unit]["multiplier"]

        # Przeliczanie z jednostki bazowej na docelową
        if target_unit != 'KG' and target_unit in conversion_factors:
            value /= conversion_factors[target_unit]["multiplier"]

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

    if conversion_type == "temperature":
        display_units = {"C", "K", "F"}
    else:
        # Wyświetl wszystkie dostępne jednostki
        display_units = set()
        for key in units:
            display_units.update(key.split("_"))

    print("Available units:", ", ".join(sorted(display_units)))
    source_unit = input("Enter source unit: ").upper()
    target_unit = input("Enter target unit: ").upper()

    value = utils.validate_number(input("Enter the value to be converted: "))

    if source_unit == target_unit:
        print(f"{value} {source_unit} to {value:.2f} {target_unit}")
        return

    if value is None:
        return

    outcome = calculate(value, source_unit, target_unit, conversion_type)
    if outcome is not None:
        print(f"{value} {source_unit} to {outcome:.2f} {target_unit}")

