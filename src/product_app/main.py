# Importación de librerías necesarias
import tkinter as tk  # Para la interfaz gráfica
import re  # Para expresiones regulares
from tkinter import BOTH, ttk, messagebox  # Componentes específicos de tkinter
import csv  # Para manejo de archivos CSV
from tempfile import NamedTemporaryFile  # Para manejo de archivos temporales
import shutil  # Para operaciones de archivos

# Expresiones regulares para validación
regex_product = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"  # Solo letras y espacios
regex_price = r"^[0-9]+$"  # Solo números

# Clase Producto para representar los productos
class Producto:
    def __init__(self, nombre_producto, precio):
        self.nombre_producto = nombre_producto
        self.precio = precio

    def __str__(self):
        return f"Nombre: {self.nombre_producto}, Precio: {self.precio}"

# Función para inicializar el archivo CSV si no existe
def init_csv():
    try:
        # Intenta abrir el archivo para ver si existe
        with open("./products.csv", "r", encoding="utf-8") as file:
            pass
    except FileNotFoundError:
        # Si no existe, crea el archivo con los encabezados
        with open("products.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["nombre_producto", "precio"])

# Función para añadir un nuevo producto
def add_product():
    product_name = name.get()  # Obtiene el nombre del campo de entrada
    product_price = price.get()  # Obtiene el precio del campo de entrada
    # Valida que los campos no estén vacíos y cumplan con las expresiones regulares
    if product_name and product_price and (
        bool(re.fullmatch(regex_product, product_name)) and bool(re.fullmatch(regex_price, product_price))):
        producto = Producto(product_name, product_price)  # Crea un objeto Producto
        _save_product(producto)  # Guarda el producto en el CSV
        name.delete(0, tk.END)  # Limpia el campo de nombre
        price.delete(0, tk.END)  # Limpia el campo de precio
        get_products()  # Actualiza la lista de productos
    else:
        messagebox.showwarning(
            "Advertencia", "Por favor ingrese nombre y precio del producto"
        )

# Función privada para guardar un producto en el CSV
def _save_product(producto):
    with open("./products.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([producto.nombre_producto, producto.precio])

# Función para obtener y mostrar productos
def get_products(name=None):
    # Limpia el árbol (tabla) antes de cargar nuevos datos
    for i in tree.get_children():
        tree.delete(i)
    try:
        # Abre el archivo CSV y lee los productos
        with open("./products.csv", "r", encoding="utf-8") as file:
            lector_csv = csv.DictReader(file)
            for idx, row in enumerate(lector_csv):
                producto = Producto(row["nombre_producto"], row["precio"])
                # Filtra por nombre si se proporciona
                if name and producto.nombre_producto.lower().startswith(name.lower()):
                    _insert_product_to_tree(producto, idx)
                elif not name:
                    _insert_product_to_tree(producto, idx)
    except FileNotFoundError:
        pass

# Función privada para insertar un producto en el árbol (tabla)
def _insert_product_to_tree(producto, index):
    tree.insert(
        "",
        tk.END,
        iid=index,
        values=(producto.nombre_producto, producto.precio),
    )

# Función para buscar productos
def search_products():
    search_text = search_entry.get()  # Obtiene el texto de búsqueda
    get_products(search_text)  # Filtra los productos

# Función para mostrar todos los productos
def see_all_products():
    get_products("")  # Muestra todos los productos
    search_entry.delete(0, tk.END)  # Limpia el campo de búsqueda

# Función para eliminar productos seleccionados
def delete_product():
    selected_item = tree.selection()  # Obtiene los elementos seleccionados
    _delete_products_from_csv(selected_item)  # Elimina del CSV
    get_products()  # Actualiza la lista

# Función privada para eliminar productos del CSV
def _delete_products_from_csv(indices_a_eliminar):
    # Crea un archivo temporal para el proceso
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="", encoding="utf-8")
    with open("./products.csv", "r", encoding="utf-8") as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=["nombre_producto", "precio"])
        writer.writeheader()
        # Copia todas las filas excepto las seleccionadas
        for idx, row in enumerate(reader):
            if str(idx) not in indices_a_eliminar:
                writer.writerow(row)
    # Reemplaza el archivo original con el temporal
    shutil.move(tempfile.name, "./products.csv")

# Función para iniciar la edición de un producto
def start_edit():
    selected_item = tree.selection()
    if len(selected_item) > 1:
        messagebox.showwarning(
            "Advertencia", "Por favor seleccione solo un producto para editar"
        )
        return
    # Obtiene los datos del producto seleccionado
    item_data = tree.item(selected_item[0], "values")
    name.delete(0, tk.END)
    name.insert(0, item_data[0])  # Rellena el campo de nombre
    price.delete(0, tk.END)
    price.insert(0, item_data[1])  # Rellena el campo de precio
    # Cambia el estado de los botones
    add_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button.config(state=tk.DISABLED)
    see_all_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.NORMAL)
    start_edit_button.config(state=tk.DISABLED)
    global editing_item
    editing_item = selected_item[0]  # Guarda el índice del item que se está editando

# Función para guardar los cambios de la edición
def save_edit():
    global editing_item
    new_name = name.get()
    new_price = price.get()
    # Valida los nuevos datos
    if new_name and new_price and (
        bool(re.fullmatch(regex_product, new_name)) and bool(re.fullmatch(regex_price, new_price))):
        producto_editado = Producto(new_name, new_price)
        _update_product_in_csv(producto_editado, editing_item)
    else:
        messagebox.showwarning(
            "Advertencia", "Por favor ingrese nombre y precio del producto"
        )
        return
    # Limpia los campos y restaura el estado de los botones
    name.delete(0, tk.END)
    price.delete(0, tk.END)
    add_button.config(state=tk.NORMAL)
    edit_button.config(state=tk.DISABLED)
    search_button.config(state=tk.NORMAL)
    see_all_button.config(state=tk.NORMAL)
    start_edit_button.config(state=tk.NORMAL)
    editing_item = None
    get_products()  # Actualiza la lista

# Función privada para actualizar un producto en el CSV
def _update_product_in_csv(producto_actualizado, indice_a_editar):
    tempfile = NamedTemporaryFile(mode="w", delete=False, newline="", encoding="utf-8")
    with open("./products.csv", "r", encoding="utf-8") as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile, fieldnames=["nombre_producto", "precio"])
        writer.writeheader()
        # Copia todas las filas, actualizando la que se está editando
        for idx, row in enumerate(reader):
            if str(idx) == indice_a_editar:
                writer.writerow({"nombre_producto": producto_actualizado.nombre_producto, "precio": producto_actualizado.precio})
            else:
                writer.writerow(row)
    shutil.move(tempfile.name, "./products.csv")

# Inicializa el archivo CSV
init_csv()

# Configuración de la ventana principal
window = tk.Tk()
window.title("Registro de Productos")
window.configure(bg="#111")  # Fondo oscuro

editing_item = None  # Variable global para el item que se está editando

# Marco principal
div = tk.Frame(window)
div.pack(padx=20, pady=20)

# Marco para añadir/editar productos
labelframe = tk.LabelFrame(
    div,
    text="Añadir/Editar Producto",
    bg="#222",  # Fondo oscuro
    font=("Verdana", 18),
    fg="#f8f8ff",  # Texto blanco
    bd=5,
    padx=10,
    pady=10,
    relief="groove",
)
labelframe.pack()

# Marco para el campo de nombre
name_frame = tk.Frame(labelframe, bg="#222")
name_frame.pack(padx=15, pady=(7.5, 7.5))
tk.Label(
    name_frame, text="Nombre", bg="#222", fg="#f8f8ff", font=("Verdana", 12)
).pack()
name = tk.Entry(name_frame)
name.pack()

# Marco para el campo de precio
price_frame = tk.Frame(labelframe, bg="#222")
price_frame.pack(padx=15, pady=(7.5, 30))
tk.Label(
    price_frame, text="Precio", bg="#222", fg="#f8f8ff", font=("Verdana", 12)
).pack()
price = tk.Entry(price_frame)
price.pack()

# Marco para los botones de acción
button_frame = tk.Frame(labelframe, bg="#222")
button_frame.pack(pady=(10, 0))

# Botón para añadir producto
add_button = tk.Button(
    button_frame,
    text="Añadir Producto",
    command=add_product,
    bg="#f8f8ff",  # Fondo blanco
    fg="#111",  # Texto oscuro
    bd=0,
)
add_button.pack(side=tk.LEFT, padx=5)

# Botón para iniciar edición
start_edit_button = tk.Button(
    button_frame,
    text="Editar Producto",
    command=start_edit,
    bg="#FFA500",  # Naranja
    fg="#111",
    bd=0,
    state=tk.DISABLED  # Inicialmente deshabilitado
)
start_edit_button.pack(side=tk.LEFT, padx=5)

# Botón para guardar edición
edit_button = tk.Button(
    button_frame,
    text="Guardar Edición",
    command=save_edit,
    bg="#4CAF50",  # Verde
    fg="#111",
    bd=0,
    state=tk.DISABLED,  # Inicialmente deshabilitado
)
edit_button.pack(side=tk.LEFT, padx=5)

# Marco para la búsqueda
search_frame = tk.Frame(window, bg="#111")
search_frame.pack(pady=(0, 10))

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Buscar", command=search_products)
search_button.pack(side=tk.LEFT, padx=5)

see_all_button = tk.Button(search_frame, text="Mostrar todos", command=see_all_products)
see_all_button.pack()

# Marco para el botón de eliminar
delete_frame = tk.Frame(window, bg="#111")
delete_frame.pack(pady=(0, 10))

delete_button = tk.Button(
    delete_frame,
    text="Eliminar Seleccionado",
    command=delete_product,
    bg="#F44336",  # Rojo
    fg="#111",
    bd=0,
    state=tk.DISABLED  # Inicialmente deshabilitado
)
delete_button.pack(side=tk.LEFT, padx=5)

# Configuración del Treeview (tabla)
tree = ttk.Treeview(
    window, columns=("name", "price"), show="headings", selectmode="extended"
)
tree.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
tree.heading("name", text="Nombre", anchor="center")
tree.heading("price", text="Precio", anchor="center")

# Estilo del Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="#333",  # Fondo oscuro
    foreground="#f8f8ff",  # Texto blanco
    fieldbackground="#333",
    bordercolor="#444",
    borderwidth=1,
)

style.configure("Treeview.Heading",
    background="#222",  # Fondo más oscuro para los encabezados
    foreground="#f8f8ff",
    font=("Verdana", 10, "bold"),
    relief="groove"
)

# Función para manejar la selección en el Treeview
def on_tree_select(event):
    selected = tree.selection()
    if selected:
        # Habilita botones si hay selección
        delete_button.config(state=tk.NORMAL)
        start_edit_button.config(state=tk.NORMAL)
    else:
        # Deshabilita botones si no hay selección
        delete_button.config(state=tk.DISABLED)
        start_edit_button.config(state=tk.DISABLED)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Carga inicial de productos
get_products()

# Inicia el bucle principal de la aplicación
window.mainloop()
