import Conversions.constant as constant
import Conversions.currency as currency
from utils import utils
import tkinter as tk


def main_menu(window):
    utils.clear_window(window)
    tk.Button(window, text="Constant Conversion", command=lambda: constant.choose_conversion(window)).pack()
    tk.Button(window, text="Currency Conversion", command=lambda: currency.currency_conversion(window)).pack()
    tk.Button(window, text="Add New Unit", command=lambda: utils.add_new_unit(window)).pack()
    tk.Button(window, text="Exit", command=window.quit).pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conversion Application")
    root.geometry("400x300")
    main_menu(root)
    root.mainloop()
