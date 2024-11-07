import tkinter as tk
from tkinter import filedialog
import sqlite3


#TODO: habria que pensar en tags tambien no?
class Feature:
    def _init_(self, name, description):
        self.name = name
        self.description = description
        self.scenarios = []

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

class Scenario:
    def _init_(self, name):
        self.name = name
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

class Step:
    def _init_(self, keyword, text):
        self.keyword = keyword
        self.text = text



def initialize_database():
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

    conn.commit()
    conn.close()

# Llamar a la función para inicializar la base de datos
initialize_database()

def search_predictive(query):
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()

    # Buscar coincidencias en la tabla Feature
    cursor.execute("SELECT name FROM Feature WHERE name LIKE ?", ('%' + query + '%',))
    features = cursor.fetchall()

    # Buscar coincidencias en la tabla Scenario
    cursor.execute("SELECT name FROM Scenario WHERE name LIKE ?", ('%' + query + '%',))
    scenarios = cursor.fetchall()

    # Buscar coincidencias en la tabla Step
    cursor.execute("SELECT text FROM Step WHERE text LIKE ?", ('%' + query + '%',))
    steps = cursor.fetchall()

    conn.close()

    return {
        "features": features,
        "scenarios": scenarios,
        "steps": steps
    }


def create_feature(frame, texts):
    # Aquí puedes agregar el código para la funcionalidad "Crear"
    pass

def consult_feature(frame, texts):
    # Aquí puedes agregar el código para la funcionalidad "Consultar"
    pass

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

    # Función para aceptar la selección del archivo
    def accept_file():
        file_path = file_path_var.get()
        if file_path:
            print(f"Archivo aceptado: {file_path}")
            # Aquí se puede definir el proceso de carga del archivo
            feature = process_feature_file(file_path)
            if feature != False:
                store_feature_in_db(feature)
            else:
                print("ERROR: en accept_file() porque la feature devolvio False")

    # Crear el botón para cargar el archivo
    btn_load_file = tk.Button(frame, text=texts["load_file"], command=load_file)
    btn_load_file.pack(pady=10)

    # Mostrar la ruta y nombre del archivo cargado
    label_file_path = tk.Label(frame, textvariable=file_path_var)
    label_file_path.pack(pady=10)

    label_file_name = tk.Label(frame, textvariable=file_name_var)
    label_file_name.pack(pady=10)

    # Crear los botones "Aceptar" y "Cancelar"
    btn_accept = tk.Button(frame, text=texts["accept"], command=accept_file)
    btn_accept.pack(side=tk.LEFT, padx=10)

    btn_cancel = tk.Button(frame, text=texts["cancel"], command=cancel_file)
    btn_cancel.pack(side=tk.LEFT, padx=10)

def process_feature_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        print("process_feature_file start:")
        #print(file)
        current_feature = None
        current_scenario = None
        #Verificamos que el fichero no de ningun error
        try:
            for line in file:
                line = line.strip()
                print(line)

                if line.startswith("Feature:"):
                    #vamos a controlar si no existe el campo description
                    try:
                        name = line[len("Feature:"):].strip()
                        print(f"  el nombre de la feature es {name}")
                        description = next(file).strip()
                        print(f"  la descripcion de la feature '{name}' es '{description}'")
                        #featuretmp = Feature(name, description)
                        featuretmp = CFeature(name)
                        current_feature = featuretmp
                        print(f"  la informacion de la feature es {current_feature}")
                    except Exception as err:
                        print(f"Unexpected {err=}, {type(err)=}")
                        raise



                elif line.startswith("Scenario:"):
                    name = line[len("Scenario:"):].strip()
                    print(f"  el nombre del escenario es '{name}'")
                    current_scenario = Scenario(name)
                    print(f"  el nombre del escenario es '{name}'")
                    if current_feature:
                        current_feature.add_scenario(current_scenario)
                        print(f"  añadimos el escenario {name} a {current_feature.name}")

                elif any(line.startswith(keyword) for keyword in ["Given", "When", "Then", "And", "But"]):
                    print(f"  ahora procesamos el step {keyword}")
                    keyword, text = line.split(maxsplit=1)
                    step = Step(keyword, text)
                    print(f"  procesamos el step {step}")
                    if current_scenario:
                        current_scenario.add_step(step)
                        print(f"  añadimos el step {step} a {current_scenario.name}")


            return current_feature
        except:
            print("ERROR: formato del feature incorrecto")
            return False

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

    cursor.execute("INSERT INTO Feature (name, description) VALUES (?, ?)", (feature.name, feature.description))
    feature_id = cursor.lastrowid

    for scenario in feature.scenarios:
        cursor.execute("INSERT INTO Scenario (feature_id, name) VALUES (?, ?)", (feature_id, scenario.name))
        scenario_id = cursor.lastrowid

        for step in scenario.steps:
            cursor.execute("INSERT INTO Step (scenario_id, keyword, text) VALUES (?, ?, ?)", (scenario_id, step.keyword, step.text))

    conn.commit()
    conn.close()

# Ejemplo de uso
query = "login"
results = search_predictive(query)
print("Features:", results["features"])
print("Scenarios:", results["scenarios"])
print("Steps:", results["steps"])