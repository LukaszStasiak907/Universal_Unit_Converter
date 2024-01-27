import Conversions.constant as constant
import Conversions.currency as currency
from utils import utils
import tkinter as tk


def main_menu(window):
    utils.clear_window(window)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    tk.Label(window, text="Welcome to the Universal Unit Converter Application", font=("Helvetica", 12)).grid(row=0, column=0, sticky="nsew")
    tk.Button(window, text="Constant Conversion", command=lambda: constant.choose_conversion(window)).grid(row=1, column=0, sticky="nsew")
    tk.Button(window, text="Currency Conversion", command=lambda: currency.currency_conversion(window)).grid(row=2, column=0, sticky="nsew")
    tk.Button(window, text="Add New Unit", command=lambda: utils.add_new_unit(window)).grid(row=3, column=0, sticky="nsew")
    tk.Button(window, text="Exit", command=window.quit).grid(row=4, column=0, sticky="nsew")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Universal Unit Converter Application")
    root.geometry("400x300")
    main_menu(root)
    root.mainloop()
