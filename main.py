import tkinter as tk
from tkinter import ttk
from utils import validate_number, load_conversion_factors, add_new_unit
from Conversions import constant, currency

def main():
    root = tk.Tk()
    root.title("Konwerter Jednostek")

    def show_frame(frame):
        frame.tkraise()

    # Ramki dla różnych typów konwersji
    main_frame = ttk.Frame(root)
    constant_frame = constant.get_constant_frame(root, "mass")  # Przykład dla "mass", możesz zmienić na inny typ
    currency_frame = currency.get_currency_frame(root)

    # Funkcja do aktualizowania ramki konwersji stałych wartości
    def update_constant_frame(conversion_type):
        new_frame = constant.get_constant_frame(root, conversion_type)
        new_frame.grid(row=0, column=0, sticky="nsew")
        show_frame(new_frame)

    # Layout ramki głównej
    main_frame.grid(row=0, column=0, sticky='nsew')
    constant_frame.grid(row=0, column=0, sticky='nsew')
    currency_frame.grid(row=0, column=0, sticky='nsew')

    # Elementy interfejsu w ramce głównej
    ttk.Label(main_frame, text="Wybierz typ konwersji:").pack()
    conversion_type_combobox = ttk.Combobox(main_frame, values=["mass", "temperature", "length", "custom"])
    conversion_type_combobox.pack()
    conversion_type_combobox.bind("<<ComboboxSelected>>", lambda event: update_constant_frame(conversion_type_combobox.get()))

    ttk.Button(main_frame, text="Konwersja Stałych", command=lambda: update_constant_frame("mass")).pack()
    ttk.Button(main_frame, text="Konwersja Walut", command=lambda: show_frame(currency_frame)).pack()

    # Ramka do dodawania nowych jednostek
    add_unit_frame = ttk.Frame(root)
    add_unit_frame.grid(row=0, column=0, sticky='nsew')

    ttk.Label(add_unit_frame, text="Nazwa nowej jednostki:").pack()
    new_unit_name_entry = ttk.Entry(add_unit_frame)
    new_unit_name_entry.pack()

    ttk.Label(add_unit_frame, text="Nazwa jednostki docelowej:").pack()
    target_unit_name_entry = ttk.Entry(add_unit_frame)
    target_unit_name_entry.pack()

    ttk.Label(add_unit_frame, text="Współczynnik konwersji:").pack()
    multiplier_entry = ttk.Entry(add_unit_frame)
    multiplier_entry.pack()

    def add_unit():
        source_unit = new_unit_name_entry.get().upper()
        target_unit = target_unit_name_entry.get().upper()
        multiplier = validate_number(multiplier_entry.get())
        if multiplier:
            add_new_unit(source_unit, target_unit, multiplier)
            tk.messagebox.showinfo("Sukces", f"Jednostka {source_unit} została dodana.")

    ttk.Button(add_unit_frame, text="Dodaj nową jednostkę", command=add_unit).pack()
    ttk.Button(main_frame, text="Dodaj Nową Jednostkę", command=lambda: show_frame(add_unit_frame)).pack()

    ttk.Button(main_frame, text="Powrót do Menu", command=lambda: show_frame(main_frame)).pack()
    ttk.Button(add_unit_frame, text="Powrót do Menu", command=lambda: show_frame(main_frame)).pack()
    ttk.Button(currency_frame, text="Powrót do Menu", command=lambda: show_frame(main_frame)).pack()

    # Wyświetlenie ramki głównej
    show_frame(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
