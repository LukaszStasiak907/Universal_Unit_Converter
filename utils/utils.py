import json


def validate_number(input_str):
    try:
        return float(input_str)
    except ValueError:
        print("This is not a valid number.")
        return None


def load_conversion_factors(conversion_type):
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    with open(json_file, 'r') as file:
        conversion_factors = json.load(file)
    return conversion_factors


def add_new_unit():
    converter_custom = 'Unit_Converters/converter_custom.json'
    try:
        with open(converter_custom, 'r') as file:
            try:
                custom_units = json.load(file)
                if not isinstance(custom_units, dict):  # Sprawdza, czy załadowany JSON to słownik
                    print("Invalid content in custom_units.json. Resetting file to an empty dictionary.")
                    custom_units = {}
            except json.JSONDecodeError:
                print("Empty or invalid JSON in custom_units.json. Creating a new dictionary.")
                custom_units = {}
    except FileNotFoundError:
        print(f"{converter_custom} file not found. Creating a new file.")
        custom_units = {}

    source_unit = input("Enter the name of the new unit (e.g., 'My Unit'): ").upper()
    target_unit = input("Enter the target unit this corresponds to (e.g., 'meter or whatever you want e.g. My 2nd unit'): ").upper()
    multiplier = validate_number(input(f"Enter how many {target_unit}s make one {source_unit}: "))

    if multiplier is None or multiplier == 0:
        print("Invalid multiplier. The new unit was not added.")
        return

    # Dodaje konwersję z jednostki źródłowej na docelową
    forward_key = f"{source_unit}_{target_unit}"
    custom_units[forward_key] = {"multiplier": multiplier}

    # Dodaje odwrotną konwersję z jednostki docelowej na źródłową
    backward_key = f"{target_unit}_{source_unit}"
    custom_units[backward_key] = {"multiplier": 1 / multiplier}

    with open(converter_custom, 'w') as file:
        json.dump(custom_units, file, indent=4)

    print(f"Units {source_unit} <=> {target_unit} have been added with multipliers {multiplier} and {1/multiplier} respectively.")
