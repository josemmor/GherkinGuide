import tkinter as tk
import json
from tkinter import PhotoImage
from interfaces.features import create_feature, consult_feature, import_feature
import interfaces.buscarfeatures as buscarfeatures

# variable general:
images_path="interfaces/images/"

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
    spain_flag = PhotoImage(file=images_path+"es.png")
    us_flag = PhotoImage(file=images_path+"us.png")
    
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

def show_about(frame, texts):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Cargar el logo de la aplicación
    app_logo = PhotoImage(file=images_path+"logo.png")

    # Crear el título de la sección
    label_title = tk.Label(frame, text=texts["about_section"], font=("Helvetica", 16))
    label_title.pack(pady=10)

    # Crear el widget de imagen
    logo_label = tk.Label(frame, image=app_logo)
    logo_label.image = app_logo  # Mantener una referencia a la imagen
    logo_label.pack(pady=10)

    # Crear el widget de texto para mostrar la información de la aplicación
    info = f"""
    {texts["version"]}:0.0.1
    {texts["creator"]}:Jose Miguel Morales
    {texts["last_updated"]}:2024-11-06
    """
    label_info = tk.Label(frame, text=info, font=("Helvetica", 12), justify=tk.LEFT)
    label_info.pack(pady=10)




def update_menu(texts):
    # Limpiar la barra de menús
    menu_bar.delete(0, tk.END)

    # Crear el menú "Features" con opciones desplegables
    features_menu = tk.Menu(menu_bar, tearoff=0)
    features_menu.add_command(label=texts["create"], command=lambda: create_feature(frame, texts))
    features_menu.add_command(label=texts["update"], command=lambda: update_feature(frame, texts))
    features_menu.add_command(label=texts["search"], command=lambda: consult_feature(frame, texts))
    features_menu.add_command(label=texts["import"], command=lambda: import_feature(frame, texts))
    menu_bar.add_cascade(label=texts["features"], menu=features_menu)

    # Añadir las opciones directamente a la raíz de la barra de menús
    menu_bar.add_command(label=texts["branches"], command=lambda: print(texts["branches"] + " selected"))
    menu_bar.add_command(label=texts["config"], command=lambda: show_language_options(frame, root, texts))
    menu_bar.add_command(label=texts["management"], command=lambda: print(texts["management"] + " selected"))
    menu_bar.add_command(label="About", command=lambda: show_about(frame, texts))


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

    # Configurar el icono de la ventana
    root.iconbitmap(images_path+"logo.ico")

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