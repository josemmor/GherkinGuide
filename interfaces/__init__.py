import tkinter as tk
import json
from tkinter import PhotoImage

def load_texts(lang):
    with open("interfaces/languages.json", "r", encoding="utf-8") as file:
        texts = json.load(file)
        return texts[lang]

def show_language_options(frame, root, texts):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()


    # Título de la sección
    label = tk.Label(frame, text=texts["language_section"], font=("Helvetica", 16))
    label.pack(pady=10)

    # Cargar las banderas
    spain_flag = PhotoImage(file="interfaces/images/es.png")
    us_flag = PhotoImage(file="interfaces/images/us.png")
    
    # Función para cambiar el idioma
    def change_language(lang):
        texts = load_texts(lang)
        root.title(texts["title"])
        update_menu(texts)
        show_language_options(frame, root, texts)
    
    # Crear los botones de selección de idioma
    btn_spanish = tk.Button(frame, image=spain_flag, text="ES", compound=tk.LEFT, command=lambda: change_language("es"))
    btn_english = tk.Button(frame, image=us_flag, text="US", compound=tk.LEFT, command=lambda: change_language("en"))

    # Empaquetar los botones
    btn_spanish.pack(side=tk.LEFT, padx=20)
    btn_english.pack(side=tk.LEFT, padx=20)

    # Mantener una referencia a las imágenes
    btn_spanish.image = spain_flag
    btn_english.image = us_flag

def update_menu(texts):
    # Limpiar la barra de menús
    menu_bar.delete(0, tk.END)

    # Añadir las opciones directamente a la raíz de la barra de menús
    menu_bar.add_command(label=texts["features"], command=lambda: print(texts["features"] + " selected"))
    menu_bar.add_command(label=texts["branches"], command=lambda: print(texts["branches"] + " selected"))
    menu_bar.add_command(label=texts["config"], command=lambda: show_language_options(frame, root, texts))
    menu_bar.add_command(label=texts["management"], command=lambda: print(texts["management"] + " selected"))

def start_application():
    global menu_bar, frame, root
    # Seleccionar el idioma (por ejemplo, "en" para inglés, "es" para español)
    lang = "es"

    # Cargar los textos del archivo JSON
    texts = load_texts(lang)

    # Crear la ventana principal
    root = tk.Tk()
    root.title(texts["title"])
    root.geometry("700x500")

    # Crear la barra de menús
    menu_bar = tk.Menu(root)

    # Añadir las opciones directamente a la raíz de la barra de menús
    update_menu(texts)

    # Asignar la barra de menús a la ventana principal
    root.config(menu=menu_bar)

    # Crear un Frame para centrar los contenidos
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Ejecutar la aplicación
    root.mainloop()