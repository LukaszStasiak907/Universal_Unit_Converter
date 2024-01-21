import Conversions.constant as constant
import Conversions.currency as currency
from utils import utils


def main_menu():
    print("Choose type of conversion or action")
    print("1. Constant")
    print("2. Currency")
    print("3. Add new unit.")
    print("4. Exit program")
    choice = input("Enter option number:")
    return choice


def main():
    while True:
        choice = main_menu()
        if choice == "1":
            constant.choose_conversion()
        elif choice == "2":
            currency.fetch_currencies()
            currency.currency_conversion()
        elif choice == "3":
            utils.add_new_unit()
        elif choice == "4":
            print("You exit the program.")
            break
        else:
            print("Incorrect choice, try again!")


if __name__ == "__main__":
    main()
