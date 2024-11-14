

import sqlite3
from interfaces.buscarfeatures import *
from interfaces.class_feature import *
from interfaces.importfeature import *




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
    buscar_features(frame, texts)




def limpiar_etiquetas(frame):
    """Limpia todas las etiquetas dentro de un frame.

    Args:
        frame (tk.Frame): El frame que contiene las etiquetas.
    """

    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text="")

def crear_etiqueta_resultado(frame, texto):
    """Crea una etiqueta en el frame especificado con el texto dado.

    Args:
        frame (tk.Frame): El frame donde se colocará la etiqueta.
        texto (str): El texto que se mostrará en la etiqueta.
    """

    label = tk.Label(frame, text=texto)
    label.pack(pady=10)
    return label

# Ejemplo de uso
query = "login"
results = search_predictive(query)
print("Features:", results["features"])
print("Scenarios:", results["scenarios"])
print("Steps:", results["steps"])
