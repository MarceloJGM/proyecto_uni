import tkinter as tk
from tkinter import ttk
import csv


def add_product():
    product_name = name.get()
    product_price = price.get()
    if product_name and product_price:
        with open(
            "./products.csv",
            "a",
            newline="",
            encoding="utf-8",
        ) as file:
            escritor_csv = csv.writer(file)
            escritor_csv.writerow([product_name, product_price])
    name.delete(0, tk.END)
    price.delete(0, tk.END)
    get_products()

def get_products(name=None):
    for i in tree.get_children():
        tree.delete(i)
    with open(
        "./products.csv",
        "r",
        encoding="utf-8",
    ) as file:
        lector_csv = csv.DictReader(file)
        for product in lector_csv:
            if name:
                if product["nombre_producto"].lower().startswith(name):
                    tree.insert("", 0, values=(product["nombre_producto"], product["precio"]))
            else:
                tree.insert("", 0, values=(product["nombre_producto"], product["precio"]))



def search_products():
    search_text = search_entry.get().lower()
    get_products(search_text)

window = tk.Tk()
window.title("Registro de Productos")
window.configure(bg="#111")

div = tk.Frame(window)
div.pack(padx=20, pady=20)

labelframe = tk.LabelFrame(
    div,
    text="Añadir Producto",
    bg="#222",
    font=("Verdana", 18),
    fg="#f8f8ff",
    bd=5,
    padx=10,
    pady=10,
    relief="groove",
)
labelframe.pack()

name_frame = tk.Frame(labelframe, bg="#222")
name_frame.pack(padx=15, pady=(7.5, 7.5))
tk.Label(
    name_frame, text="Nombre", bg="#222", fg="#f8f8ff", font=("Verdana", 12)
).pack()
name = tk.Entry(name_frame)
name.pack()

price_frame = tk.Frame(labelframe, bg="#222")
price_frame.pack(padx=15, pady=(7.5, 30))
tk.Label(
    price_frame, text="Precio", bg="#222", fg="#f8f8ff", font=("Verdana", 12)
).pack()
price = tk.Entry(price_frame)
price.pack()

button = tk.Button(
    labelframe,
    text="Añadir Producto",
    command=add_product,
    bg="#f8f8ff",
    fg="#111",
    bd=0,
)
button.pack()

search_frame = tk.Frame(window, bg="#111")
search_frame.pack(pady=(0, 30))

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(search_frame, text="Buscar", height=0, command=search_products)
search_button.pack(side='right')

tree = ttk.Treeview(window, columns=("name", "price"), show="headings")
tree.pack()
tree.heading("name", text="Nombre", anchor="center")
tree.heading("price", text="Precio", anchor="center")

get_products()

window.mainloop()

