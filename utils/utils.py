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
    pass
