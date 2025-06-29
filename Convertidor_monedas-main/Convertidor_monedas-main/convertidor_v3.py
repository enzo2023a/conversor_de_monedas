import tkinter as tk
from tkinter import ttk, Menu
from PIL import Image, ImageTk
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# Diccionario de tasas de cambio
cambio = {
    "ARS": {"ARS": 1.0, "USD": 0.00086, "EUR": 0.00073, "CNY": 0.00061, "GBP": 0.00063},
    "USD": {"USD": 1.0, "ARS": 1164, "EUR": 0.86, "CNY": 7.17, "GBP": 0.73},
    "EUR": {"EUR": 1.0, "ARS": 1364, "USD": 1.16, "CNY": 8.34, "GBP": 0.85},
    "CNY": {"CNY": 1.0, "ARS": 163, "USD": 0.14, "EUR": 0.12, "GBP": 0.10},
    "GBP": {"GBP": 1.0, "ARS": 1600, "USD": 1.36, "EUR": 1.17, "CNY": 9.77}
}

# Diccionario de banderas
banderas = {
    "ARS": os.path.join(BASE_DIR, "banderas", "ARS.png"),
    "USD": os.path.join(BASE_DIR, "banderas", "USD.png"),
    "EUR": os.path.join(BASE_DIR, "banderas", "EUR.png"),
    "CNY": os.path.join(BASE_DIR, "banderas", "CNY.png"),
    "GBP": os.path.join(BASE_DIR, "banderas", "GBP.png")
}


# Crear ventana
app = tk.Tk()
app.title("Conversor Monetario")
app.geometry("400x300")
app.configure(bg="#f7f7f7")
app.resizable(False,False)

# funcion claro - oscuro
def menu_tema_presionado():
    valor_tema = tema_elegido.get()
    if valor_tema == 1:
        print("Tema claro establecido.")
        app.configure(bg="#f7f7f7")
        cantidad.config(bg="#f7f7f7",fg="#333333")

        for i, (label_text, seleccion, default) in enumerate([
            ("Moneda de origen:", seleccion_origen, opciones[0]),
            ("Moneda de destino:", seleccion_destino, opciones[1])
        ]):
            origen_destino = tk.Label(app, text=label_text, font=label_font, bg="#f7f7f7", fg="#333333")
            origen_destino.grid(row=i+1, column=0, padx=5, pady=5)
            combo = ttk.Combobox(app, textvariable=seleccion, values=opciones, state="readonly")
            combo.grid(row=i+1, column=1, padx=5, pady=5)
            label_bandera = tk.Label(app, image=imagenes_tk[default], bg="#f7f7f7")
            label_bandera.grid(row=i+1, column=2, padx=5, pady=5 )
            combo.bind("<<ComboboxSelected>>", lambda event, c=combo, l=label_bandera: actualizar_bandera(c, l))

        valor_label.config(bg='#f7f7f7', fg='#333333')
    
    elif valor_tema == 2:
        print("Tema oscuro establecido.")
        app.configure(bg='#333333')
        cantidad.config(bg="#333333",fg="#f7f7f7")

        for i, (label_text, seleccion, default) in enumerate([
            ("Moneda de origen:", seleccion_origen, opciones[0]),
            ("Moneda de destino:", seleccion_destino, opciones[1])
        ]):
            origen_destino = tk.Label(app, text=label_text, font=label_font, bg="#333333", fg="#f7f7f7")
            origen_destino.grid(row=i+1, column=0, padx=5, pady=5)
            combo = ttk.Combobox(app, textvariable=seleccion, values=opciones, state="readonly")
            combo.grid(row=i+1, column=1, padx=5, pady=5)
            label_bandera = tk.Label(app, image=imagenes_tk[default], bg="#333333")
            label_bandera.grid(row=i+1, column=2, padx=5, pady=5 )
            combo.bind("<<ComboboxSelected>>", lambda event, c=combo, l=label_bandera: actualizar_bandera(c, l))

        
        valor_label.config(bg='#333333', fg='#f7f7f7')

#BARRA MENU
barra_menu = Menu()
menu_opciones = Menu(barra_menu, tearoff=False)
menu_tema = Menu(barra_menu, tearoff=False)
tema_elegido = tk.IntVar()
# color tema
tema_elegido.set(1) # Opción seleccionada por defecto ("Claro").
menu_tema.add_radiobutton(
    label='claro ☀️',
    variable=tema_elegido,
    value=1,
    command=menu_tema_presionado,
    accelerator='Ctrl+c'
)
menu_tema.add_radiobutton(
    label='oscuro 🌙',
    value=2,
    variable=tema_elegido,
    command=menu_tema_presionado,
    accelerator='Ctrl+o'

)
menu_opciones.add_cascade(menu=menu_tema, label="Tema")
barra_menu.add_cascade(menu=menu_opciones, label='opciones')
app.config(menu=barra_menu)

# Fuentes
label_font = ('elephant', 11, 'underline')
entry_font = ('elephant', 12)
button_font = ('constantia', 10, 'bold')


# Cargar imágenes de banderas
imagenes_tk = {moneda: ImageTk.PhotoImage(Image.open(ruta).resize((30, 20), Image.Resampling.LANCZOS))
                for moneda, ruta in banderas.items()}

# Función para actualizar banderas
def actualizar_bandera(combo, label):
    moneda = combo.get()
    label.configure(image=imagenes_tk[moneda])
    label.image = imagenes_tk[moneda]

# Función para convertir
def convertir():
    try:
        cantidad = float(entry_cantidad.get())
        if cantidad < 0:
            valor_label.config(text="ERROR!: Ingresá un valor positivo")
        else:
            moneda_origen = seleccion_origen.get()
            moneda_destino = seleccion_destino.get()
            resultado = cantidad * cambio[moneda_origen][moneda_destino]
            # valor_label.config(text=resultado)
            valor_label.config(text=f"{cantidad:.2f} {moneda_origen} = {resultado:.2f} {moneda_destino}")
    except ValueError:
        valor_label.config(text="ERROR!: Ingresá un número válido")

# Lista de monedas
opciones = ["ARS", "USD", "EUR", "CNY", "GBP"]

# Entrada de cantidad
cantidad =tk.Label(app, text="Cantidad:", font=label_font, bg="#f7f7f7", fg="#333333")
cantidad.grid(row=0, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(app, font=entry_font, width=12)
entry_cantidad.grid(row=0, column=1, columnspan=1, padx=5, pady=5)

# Combobox y banderas
seleccion_origen = tk.StringVar(value=opciones[0])
seleccion_destino = tk.StringVar(value=opciones[1])

for i, (label_text, seleccion, default) in enumerate([
    ("Moneda de origen:", seleccion_origen, opciones[0]),
    ("Moneda de destino:", seleccion_destino, opciones[1])
]):
    origen_destino = tk.Label(app, text=label_text, font=label_font, bg="#f7f7f7", fg="#333333")
    origen_destino.grid(row=i+1, column=0, padx=5, pady=5)
    combo = ttk.Combobox(app, textvariable=seleccion, values=opciones, state="readonly")
    combo.grid(row=i+1, column=1, padx=5, pady=5)
    label_bandera = tk.Label(app, image=imagenes_tk[default], bg="#f7f7f7")
    label_bandera.grid(row=i+1, column=2, padx=5, pady=5 )
    combo.bind("<<ComboboxSelected>>", lambda event, c=combo, l=label_bandera: actualizar_bandera(c, l))

# Botón convertir
tk.Button(app, text="Convertir", font=button_font, command=convertir, bg="#4caf50").grid(row=3, column=0, columnspan=3, pady=10)

# Etiqueta resultado
valor_label = tk.Label(app, text="Conversión", font=label_font, fg="#333333", relief='ridge', bd=1, padx=15, pady=15)
valor_label.grid(row=4, column=0, columnspan=3, pady=10)

#accelerator
app.bind_all("<Control-c>", menu_tema_presionado)
app.bind_all("<Control-o>", menu_tema_presionado)
app.mainloop()