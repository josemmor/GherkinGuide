import tkinter as tk
from tkinter import filedialog
from interfaces.buscarfeatures import *

#Visualizacion en la ventana de la importacion
def import_feature(frame, texts):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Título de la sección
    label = tk.Label(frame, text=texts["import_section"], font=("Helvetica", 16))
    label.pack(pady=10)

    # Variables para almacenar la ruta y nombre del archivo
    file_path_var = tk.StringVar()
    file_name_var = tk.StringVar()

    def crear_etiqueta_resultado(frame, texto):
        """Crea una etiqueta en el frame especificado con el texto dado.

        Args:
            frame (tk.Frame): El frame donde se colocará la etiqueta.
            texto (str): El texto que se mostrará en la etiqueta.
        """

        label = tk.Label(frame, text=texto)
        label.pack(pady=10)
        return label

    # Función para cargar el archivo
    def load_file():
        file_path = filedialog.askopenfilename(filetypes=[("Feature files", "*.feature")])
        if file_path:
            file_path_var.set(file_path)
            file_name_var.set(file_path.split("/")[-1])

    # Función para cancelar la selección del archivo
    def cancel_file():
        file_path_var.set("")
        file_name_var.set("")
        # Limpiamos las etiquetas directamente
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text="")

    # Función para aceptar la selección del archivo
    def accept_file():
        file_path = file_path_var.get()
        if file_path:
            print(f"Archivo aceptado: {file_path}")
            # Aquí se puede definir el proceso de carga del archivo
            feature = process_feature_file(file_path)
            if feature != False:
                store_feature_in_db(feature)
                print("Guardado en la base de datos correctamente")
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(text="")
                label_file_name = crear_etiqueta_resultado(frame, feature.name + ".feature " + texts["load_success"])


            else:
                label_file_name = crear_etiqueta_resultado(frame, text=texts["error_load"])
                print("ERROR: en accept_file() porque la feature devolvio False")

    # Crear el botón para cargar el archivo
    btn_load_file = tk.Button(frame, text=texts["load_file"], command=load_file)
    btn_load_file.pack(pady=10)

    # Mostrar la ruta y nombre del archivo cargado
    label_file_path = tk.Label(frame, textvariable=file_path_var)
    label_file_path.pack(pady=10)

    #label_file_name = tk.Label(frame, textvariable=file_name_var)
    #label_file_name.pack(pady=10)

    # Crear los botones "Aceptar" y "Cancelar"
    btn_accept = tk.Button(frame, text=texts["accept"], command=accept_file)
    btn_accept.pack(side=tk.LEFT, padx=10)

    btn_cancel = tk.Button(frame, text=texts["cancel"], command=cancel_file)
    btn_cancel.pack(side=tk.LEFT, padx=10)

def process_feature_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        if file:
            print("process_feature_file start:")
            current_feature = None
            current_scenario = None
            previous_keyword = None  # Para almacenar el último keyword principal
            
            try:
                for line in file: 
                    line = line.strip()
                    print(f"*'{line}'*")

                    # Procesamos Feature
                    if line.startswith("Feature:"):
                        name = line[len("Feature:"):].strip()
                        print(f"  el nombre de la feature es {name}")
                        try:
                            description = next(file).strip()
                            print(f"  la descripcion de la feature '{name}' es '{description}'")
                        except StopIteration:
                            description = ""
                            print("  la feature no tiene descripcion")

                        current_feature = Feature(name, description)
                        print(f"  la informacion de la feature es {current_feature}")
                        
                    # Procesamos Scenario    
                    elif line.startswith("Scenario:"):
                        name = line[len("Scenario:"):].strip()
                        print(f"  el nombre del escenario es '{name}'")
                        current_scenario = Scenario(name)
                        if current_feature:
                            current_feature.add_scenario(current_scenario)
                            print(f"  añadimos el escenario '{name}' a '{current_feature.name}'")

                    # Procesamos Steps    
                    elif any(line.startswith(keyword) for keyword in ["Given", "When", "Then", "And", "But"]):
                        try:
                            keyword, text = line.split(" ", maxsplit=1)

                            # Si el keyword es "And" o "But", usa el último keyword principal
                            if keyword in ["And", "But"] and previous_keyword:
                                keyword = previous_keyword
                            elif keyword in ["Given", "When", "Then"]:
                                # Actualizar el último keyword principal
                                previous_keyword = keyword
                            
                            step = Step(keyword, text)
                            if current_scenario:
                                current_scenario.add_step(step)
                                print(f"  añadimos el step '{text}' con el keyword '{keyword}' a {current_scenario.name}")
                        except ValueError:
                            print(f"Error al procesar el step: {line}")
                            return False
                    else:
                        print(f"------> NO SABEMOS QUE ES ESTO: '{line}'------")

                return current_feature
            except:
                print("ERROR: formato del feature incorrecto")
                return False
        else:
            print("No se cargo correctamente el fichero")

    


def store_feature_in_db(feature):
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Feature (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Scenario (
        id INTEGER PRIMARY KEY,
        feature_id INTEGER,
        name TEXT,
        FOREIGN KEY(feature_id) REFERENCES Feature(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Step (
        id INTEGER PRIMARY KEY,
        scenario_id INTEGER,
        keyword TEXT,
        text TEXT,
        FOREIGN KEY(scenario_id) REFERENCES Scenario(id)
    )
    """)

    # Verificar si la feature ya existe
    cursor.execute("SELECT id FROM Feature WHERE name = ?", (feature.name,))
    existing_feature = cursor.fetchone()

    if existing_feature:
        feature_id = existing_feature[0]
        print(f"La feature '{feature.name}' ya existe. Actualizando...")
    else:    
        cursor.execute("INSERT INTO Feature (name, description) VALUES (?, ?)", (feature.name, feature.description))
        feature_id = cursor.lastrowid


    for scenario in feature.scenarios:
        # Verificar si el escenario ya existe
        cursor.execute("SELECT id FROM Scenario WHERE feature_id = ? AND name = ?", (feature_id, scenario.name,))
        existing_scenario = cursor.fetchone()

        if existing_scenario:
            scenario_id = existing_scenario[0]
            print(f"El escenario '{scenario.name}' ya existe. Actualizando...")
        else:    
            cursor.execute("INSERT INTO Scenario (feature_id, name) VALUES (?, ?)", (feature_id, scenario.name))
            scenario_id = cursor.lastrowid

        for step in scenario.steps:
            # Verificar si el step ya existe
            cursor.execute("SELECT id FROM Step WHERE scenario_id = ? AND keyword = ? AND text = ?", (scenario_id, step.keyword, step.text))
            existing_step = cursor.fetchone()

            if existing_step:
                step_id = existing_step[0]
                print(f"El step '{step.text}' ya existe en el escenario '{scenario.name}'. Actualizando...")
            else:    
                cursor.execute("INSERT INTO Step (scenario_id, keyword, text) VALUES (?, ?, ?)", (scenario_id, step.keyword, step.text))
                print(f"Guardando el step '{step.text}' en el escenario '{scenario.name}'")
  

    conn.commit()
    conn.close()


