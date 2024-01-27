import json


def validate_number(input_str):
    """Waliduje, czy podany ciąg znaków jest liczbą i zwraca ją jako float. Zwraca None, jeśli ciąg znaków nie jest liczbą."""
    try:
        return float(input_str)
    except ValueError:
        print("To nie jest prawidłowa liczba.")
        return None


def load_conversion_factors(conversion_type):
    """Wczytuje i zwraca słownik współczynników konwersji dla podanego typu konwersji."""
    json_file = f'Unit_Converters/converter_{conversion_type}.json'
    try:
        with open(json_file, 'r') as file:
            conversion_factors = json.load(file)
        return conversion_factors
    except FileNotFoundError:
        print(f"Plik nie znaleziony: {json_file}")
        return {}
    except json.JSONDecodeError:
        print(f"Błąd w formacie JSON: {json_file}")
        return {}


def add_new_unit(source_unit, target_unit, multiplier):
    """Dodaje nową niestandardową jednostkę do pliku JSON."""
    converter_custom = 'Unit_Converters/converter_custom.json'
    try:
        with open(converter_custom, 'r') as file:
            custom_units = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        custom_units = {}

    forward_key = f"{source_unit.upper()}_{target_unit.upper()}"
    backward_key = f"{target_unit.upper()}_{source_unit.upper()}"

    custom_units[forward_key] = {"multiplier": multiplier}
    custom_units[backward_key] = {"multiplier": 1 / multiplier}

    with open(converter_custom, 'w') as file:
        json.dump(custom_units, file, indent=4)
