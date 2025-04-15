import tkinter as tk

window = tk.Tk()
window.title("Registro de Productos")

labelframe = tk.LabelFrame(window, text="Añadir Producto")
labelframe.pack()

tk.Label(labelframe, text="Nombre").pack()
name = tk.Entry(labelframe)
name.pack()

tk.Label(labelframe, text="Precio").pack()
price = tk.Entry(labelframe)
price.pack()

button = tk.Button(labelframe, text="Añadir Producto", command=lambda:print("Añadido"))
button.pack()

window.mainloop()
