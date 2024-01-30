import json
import tkinter as tk


def validate_number(input_str, window, back_function):
    """Validates if the input string can be converted to a non-negative float.

    Parameters:
    input_str (str): The string to validate.
    window (tk.Tk): The tkinter window where the result (error message or back button) will be displayed.
    back_function (function): The function to be called when the back button is clicked.

    Returns:
    float or None: The converted float value if valid and non-negative, otherwise None.
    """
    try:
        value = float(input_str)
        if value < 0:
            tk.Label(window, text="Number must be non-negative.").grid(row=0, column=0, sticky="nsew")
            tk.Button(window, text="Back", command=back_function).grid(row=1, column=0, sticky="ew")
            return None
        return value
    except ValueError:
        tk.Label(window, text="This is not a valid number.").grid(row=0, column=0, sticky="nsew")
        tk.Button(window, text="Back", command=back_function).grid(row=1, column=0, sticky="ew")
        return None


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


def add_new_unit(window):
    """Sets up the GUI for adding a new unit conversion.

    This function creates input fields for the user to enter the new unit name, target unit name,
    and conversion multiplier. It also sets up the 'Add Unit' and 'Back to Main Menu' buttons.

    Parameters:
    window (tk.Tk): The tkinter window where the GUI components will be added.
    """
    clear_window(window)
    for i in range(6):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    tk.Label(window, text="Enter the name of the new unit (e.g., 'My Unit'):").grid(row=0, column=0, sticky="nsew")
    source_unit_entry = tk.Entry(window)
    source_unit_entry.grid(row=1, column=0, sticky="ew")

    tk.Label(window,
             text="Enter the target unit this corresponds to (e.g., 'meter'):").grid(row=2, column=0, sticky="nsew")
    target_unit_entry = tk.Entry(window)
    target_unit_entry.grid(row=3, column=0, sticky="ew")

    tk.Label(window, text="Enter how many target units make one source unit:").grid(row=4, column=0, sticky="nsew")
    multiplier_entry = tk.Entry(window)
    multiplier_entry.grid(row=5, column=0, sticky="ew")

    add_button = tk.Button(window,
                           text="Add Unit",
                           command=lambda: perform_add_new_unit(window, source_unit_entry.get(),
                                                                target_unit_entry.get(), multiplier_entry.get()))
    add_button.grid(row=6, column=0, sticky="ew")

    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=7, column=0, sticky="ew")


def perform_add_new_unit(window, source_unit, target_unit, multiplier_str):
    """Validates the entered multiplier and adds the new unit conversion to the custom converter file.

    Parameters:
    window (tk.Tk): The tkinter window where the GUI components will be added or updated.
    source_unit (str): The name of the source unit to be added.
    target_unit (str): The name of the target unit to which the source unit is to be converted.
    multiplier_str (str): The string representation of the conversion multiplier from source to target unit.

    Note:
    The function updates the 'converter_custom.json' file with the new conversion units and their multipliers.
    """
    # First, we validate the entered number.
    multiplier = validate_number(multiplier_str, window, lambda: add_new_unit(window))
    if multiplier is None or multiplier == 0:
        # If it's not valid, validate_number will display an error message and a back button, so we exit the function.
        return

    # Preparing the path to the file with custom converters.
    converter_custom = 'Unit_Converters/converter_custom.json'

    # Load existing custom units or create a new dictionary if the file does not exist
    try:
        with open(converter_custom, 'r') as file:
            custom_units = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        custom_units = {}

    # Define keys for new units
    forward_key = f"{source_unit.upper()}_{target_unit.upper()}"
    backward_key = f"{target_unit.upper()}_{source_unit.upper()}"

    # Add new units to the dictionary
    custom_units[forward_key] = {"multiplier": multiplier}
    custom_units[backward_key] = {"multiplier": 1 / multiplier}

    # Save the modified dictionary to a JSON file
    with open(converter_custom, 'w') as file:
        json.dump(custom_units, file, indent=4)

    # Clear the window and display a message about the successful addition of the unit
    clear_window(window)
    for i in range(3):
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(0, weight=1)

    tk.Label(window, text=f"Units {source_unit.upper()} <=> {target_unit.upper()} have been added.").grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky="nsew")

    # Add buttons to add another unit or return to the main menu.
    new_unit_button = tk.Button(window, text="Add Another Unit", command=lambda: add_new_unit(window))
    new_unit_button.grid(row=1, column=0, sticky="ew")
    back_button = tk.Button(window, text="Back to Main Menu", command=lambda: main_menu(window))
    back_button.grid(row=2, column=0, sticky="ew")


def clear_window(window):
    """Clears all widgets from the given tkinter window.

    Parameters:
    window (tk.Tk): The tkinter window to be cleared.
    """
    for widget in window.winfo_children():
        widget.destroy()


def create_dropdown_menu(window, label_text, options, label_row, menu_row):
    """Creates a dropdown menu in a tkinter window.

    Parameters:
    window (tk.Tk): The tkinter window where the dropdown menu will be added.
    label_text (str): The text to be displayed as the label for the dropdown menu.
    options (list): A list of options to be included in the dropdown menu.
    label_row (int): The row number in the grid where the label should be placed.
    menu_row (int): The row number in the grid where the dropdown menu should be placed.

    Returns:
    tk.StringVar: A variable associated with the dropdown menu, containing the currently selected option.
    """
    label = tk.Label(window, text=label_text)
    label.grid(row=label_row, column=0, sticky="ew")
    var = tk.StringVar(window)
    var.set(options[0])
    menu = tk.OptionMenu(window, var, *options)
    menu.grid(row=menu_row, column=0, sticky="ew")
    return var


def main_menu(window):
    """Clears the current tkinter window and displays the main menu.

    Parameters:
    window (tk.Tk): The tkinter window to be updated with the main menu.

    Note:
    This function imports and calls the 'main_menu' function from the 'main' module.
    """
    clear_window(window)
    import main  # Import inside the function to avoid circular dependency
    main.main_menu(window)
