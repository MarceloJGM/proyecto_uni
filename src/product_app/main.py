import tkinter as tk
import re
from tkinter import BOTH, ttk, messagebox
import csv
from tempfile import NamedTemporaryFile
import shutil


def init_csv():
    try:
        with open("./products.csv", "r", encoding="utf-8") as file:
            pass
    except FileNotFoundError:
        with open("products.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["nombre_producto", "precio"])


def add_product():
    product_name = name.get()
    product_price = price.get()
    regex_product = r"^[a-zA]+$"
    regex_price = r"^[Z0-9]+$"
    if product_name and product_price and (
        bool(re.fullmatch(regex_product, product_name)) and bool(re.fullmatch(regex_price, product_price))):
        with open("./products.csv", "a", newline="", encoding="utf-8") as file:
            escritor_csv = csv.writer(file)
            escritor_csv.writerow([product_name, product_price])
        name.delete(0, tk.END)
        price.delete(0, tk.END)
        get_products()
    else:
        messagebox.showwarning(
            "Advertencia", "Por favor ingrese nombre y precio del producto"
        )


def get_products(name=None):
    for i in tree.get_children():
        tree.delete(i)
    try:
        with open("./products.csv", "r", encoding="utf-8") as file:
            lector_csv = csv.DictReader(file)
            for idx, product in enumerate(lector_csv):
                if name:
                    if product["nombre_producto"].lower().startswith(name.lower()):
                        tree.insert(
                            "",
                            tk.END,
                            iid=idx,
                            values=(product["nombre_producto"], product["precio"]),
                        )
                else:
                    tree.insert(
                        "",
                        tk.END,
                        iid=idx,
                        values=(product["nombre_producto"], product["precio"]),
                    )

    except FileNotFoundError:
        pass


def search_products():
    search_text = search_entry.get()
    get_products(search_text)


def delete_product():
    selected_item = tree.selection()

    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="", encoding="utf-8")

    with open("./products.csv", "r", encoding="utf-8") as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=["nombre_producto", "precio"])
        writer.writeheader()

        for idx, row in enumerate(reader):
            if str(idx) not in selected_item:
                writer.writerow(row)

    shutil.move(tempfile.name, "./products.csv")
    get_products()


def start_edit():
    selected_item = tree.selection()

    if len(selected_item) > 1:
        messagebox.showwarning(
            "Advertencia", "Por favor seleccione solo un producto para editar"
        )
        return

    item_data = tree.item(selected_item[0], "values")
    name.delete(0, tk.END)
    name.insert(0, item_data[0])
    price.delete(0, tk.END)
    price.insert(0, item_data[1])

    add_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.NORMAL)
    start_edit_button.config(state=tk.DISABLED)

    global editing_item
    editing_item = selected_item[0]


def save_edit():
    global editing_item
    new_name = name.get()
    new_price = price.get()

    if not new_name or not new_price:
        messagebox.showwarning(
            "Advertencia", "Por favor ingrese nombre y precio del producto"
        )
        return

    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="", encoding="utf-8")

    with open("./products.csv", "r", encoding="utf-8") as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=["nombre_producto", "precio"])
        writer.writeheader()

        for idx, row in enumerate(reader):
            if str(idx) == editing_item:
                writer.writerow({"nombre_producto": new_name, "precio": new_price})
            else:
                writer.writerow(row)

    shutil.move(tempfile.name, "./products.csv")

    name.delete(0, tk.END)
    price.delete(0, tk.END)
    add_button.config(state=tk.NORMAL)
    edit_button.config(state=tk.DISABLED)
    search_button.config(state=tk.NORMAL)
    start_edit_button.config(state=tk.NORMAL)
    editing_item = None
    get_products()


init_csv()
window = tk.Tk()
window.title("Registro de Productos")
window.configure(bg="#111")

editing_item = None

div = tk.Frame(window)
div.pack(padx=20, pady=20)

labelframe = tk.LabelFrame(
    div,
    text="Añadir/Editar Producto",
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

button_frame = tk.Frame(labelframe, bg="#222")
button_frame.pack(pady=(10, 0))

add_button = tk.Button(
    button_frame,
    text="Añadir Producto",
    command=add_product,
    bg="#f8f8ff",
    fg="#111",
    bd=0,
)
add_button.pack(side=tk.LEFT, padx=5)

start_edit_button = tk.Button(
    button_frame,
    text="Editar Producto",
    command=start_edit,
    bg="#FFA500",
    fg="#111",
    bd=0,
    state=tk.DISABLED
)
start_edit_button.pack(side=tk.LEFT, padx=5)

edit_button = tk.Button(
    button_frame,
    text="Guardar Edición",
    command=save_edit,
    bg="#4CAF50",
    fg="#111",
    bd=0,
    state=tk.DISABLED,
)
edit_button.pack(side=tk.LEFT, padx=5)

search_frame = tk.Frame(window, bg="#111")
search_frame.pack(pady=(0, 10))

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Buscar", command=search_products)
search_button.pack(side=tk.LEFT, padx=5)

delete_frame = tk.Frame(window, bg="#111")
delete_frame.pack(pady=(0, 10))

delete_button = tk.Button(
    delete_frame,
    text="Eliminar Seleccionado",
    command=delete_product,
    bg="#F44336",
    fg="#111",
    bd=0,
    state=tk.DISABLED
)
delete_button.pack(side=tk.LEFT, padx=5)

tree = ttk.Treeview(
    window, columns=("name", "price"), show="headings", selectmode="extended"
)
tree.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
tree.heading("name", text="Nombre", anchor="center")
tree.heading("price", text="Precio", anchor="center")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="#333",
    foreground="#f8f8ff",
    fieldbackground="#333",
    bordercolor="#444",
    borderwidth=1)
# style.map("Treeview",
#     background=[("selected", "#4CAF50")],
#     foreground=[("selected", "#111")])
style.configure("Treeview.Heading",
    background="#222",
    foreground="#f8f8ff",
    font=("Verdana", 10, "bold"),
    relief="groove")

def on_tree_select(event):
    selected = tree.selection()
    if selected:
        delete_button.config(state=tk.NORMAL)
        start_edit_button.config(state=tk.NORMAL)
    else:
        delete_button.config(state=tk.DISABLED)
        start_edit_button.config(state=tk.DISABLED)


tree.bind("<<TreeviewSelect>>", on_tree_select)

get_products()

window.mainloop()
