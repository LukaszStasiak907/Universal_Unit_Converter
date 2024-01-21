def add_new_unit():
    pass


def validate_number(input_str):
    try:
        return float(input_str)
    except ValueError:
        print("This is not a valid number.")
        return None
