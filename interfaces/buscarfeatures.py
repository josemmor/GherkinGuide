import sqlite3
import tkinter as tk
from tkinter import ttk, StringVar,font
from interfaces.class_feature import *




def buscar_features(frame, texts):
    """Busca todas las features, escenarios y steps en la base de datos y muestra los resultados en un Treeview.

    Args:
        frame (tk.Frame): El frame donde se mostrará el Treeview.
        texts (dict): Diccionario con los textos a mostrar en la interfaz.
    """

    # Limpiar la ventana
    for widget in frame.winfo_children():
        widget.destroy()

    # Conexión a la base de datos
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()

    # Obtener los datos de todas las tablas
    cursor.execute("SELECT * FROM Feature")
    features = cursor.fetchall()
    cursor.execute("SELECT * FROM Scenario")
    scenarios = cursor.fetchall()
    cursor.execute("SELECT * FROM Step")
    steps = cursor.fetchall()

    # Crear variables StringVar para los desplegables
    feature_var = StringVar()
    scenario_var = StringVar()

    # Crear combobox de búsqueda de features y escenarios
    feature_label = ttk.Label(frame, text=texts["feature"])
    feature_label.grid(row=0, column=0, sticky=tk.W)
    feature_combobox = ttk.Combobox(frame, textvariable=feature_var)
    feature_combobox['values'] = [feature[1] for feature in features]
    feature_combobox.grid(row=0, column=1, sticky=tk.W)

    scenario_label = ttk.Label(frame, text=texts["scenario"])
    scenario_label.grid(row=0, column=2, sticky=tk.W)
    scenario_combobox = ttk.Combobox(frame, textvariable=scenario_var)
    scenario_combobox.grid(row=0, column=3, sticky=tk.W)

    # Asociar la función de búsqueda en tiempo real a los eventos de cambio de los combobox
    feature_combobox.bind("<<ComboboxSelected>>", lambda event: on_combo_change(event, tree, steps, scenario_var))
    scenario_combobox.bind("<<ComboboxSelected>>", lambda event: on_combo_change(event, tree, steps, scenario_var))

    # Crear Treeview y personalizarlo
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Helvetica", 10))  # Tamaño de fuente para el texto de la tabla
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="blue")

    tree = ttk.Treeview(frame, style="Treeview", columns=("Feature", "Scenario","Keyword", "Step"))
   
    tree.heading("#0", text="")  # Ocultar la primera columna
    tree.heading("Feature", text=texts["feature"])
    tree.column("Feature", width=100, anchor="w")  # Ancho mínimo de 100 píxeles
    tree.heading("Scenario", text=texts["scenario"])
    tree.heading("Keyword", text=texts["keyword"])
    tree.column("Keyword", width=100, anchor="w")  # Ancho mínimo de 100 píxeles
    tree.heading("Step", text=texts["step"])
    
    tree.column("#0", width=0, stretch=False)  # Ajustar el ancho y evitar estiramiento
    tree.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)  # Ocupará toda la fila

    def on_combo_change(event, tree, steps, scenario_var):
        feature_filter = feature_var.get()
        scenario_filter = scenario_var.get()

        # Filtrar escenarios que pertenecen a la feature seleccionada
        conn = sqlite3.connect("features.db")
        cursor = conn.cursor()

        # Obtener los escenarios que corresponden a la feature seleccionada
        cursor.execute("SELECT Scenario.name FROM Scenario INNER JOIN Feature ON Scenario.feature_id = Feature.id WHERE Feature.name = ?", (feature_filter,))
        scenarios = cursor.fetchall()
        scenario_names = [scenario[0] for scenario in scenarios]

        # Actualizar el scenario_combobox con los escenarios filtrados
        scenario_combobox['values'] = scenario_names
        scenario_combobox.config(width=50)
        scenario_combobox.set('')  # Limpiar selección del combobox

        # Filtrar y actualizar el Treeview
        filter_treeview(tree, feature_filter, scenario_filter)

        conn.close()

    def filter_treeview(tree, feature_filter, scenario_filter):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()

            # Construir la consulta SQL de forma dinámica según los filtros
            query = """
            SELECT Feature.name, Scenario.name, Step.keyword, Step.text
            FROM Step
            JOIN Scenario ON Step.scenario_id = Scenario.id
            JOIN Feature ON Scenario.feature_id = Feature.id
            WHERE Feature.name = ?
            """
            params = [feature_filter]
            if scenario_filter:  # Añadir filtro de escenario si está seleccionado
                query += " AND Scenario.name = ?"
                params.append(scenario_filter)

            # Ejecutar la consulta con los parámetros
            cursor.execute(query, params)
            data = cursor.fetchall()

            # Limpiar y llenar el Treeview con los datos filtrados
            tree.delete(*tree.get_children())
            for item in data:
                tree.insert("", "end", values=item)

            conn.close()

        except Exception as e:
            print(f"Error al filtrar los datos: {e}")

    #Insertar datos en el Treeview
    def insertar_datos(tree, features, scenarios, steps):
        tree.delete(*tree.get_children()) #Limpiar el Treeview antes de insertar datos
        for feature in features:
            feature_id = feature[0]
            feature_name = feature[1]
            for scenario in scenarios:
                if scenario[1] == feature_id:
                    scenario_id = scenario[0]
                    scenario_name = scenario[2]
        for feature in features:
            feature_id = feature[0]
            feature_name = feature[1]
            for scenario in scenarios:
                if scenario[1] == feature_id:
                    scenario_id = scenario[0]
                    scenario_name = scenario[2]
                    # Filtrar pasos por escenario
                    scenario_steps = [step for step in steps if step[1] == scenario_id]
                    for step in scenario_steps:
                        tree.insert("", "end", values=(feature_name, scenario_name, step[2], step[3]))
    
    # Función para filtrar los datos
    def filter_data(tree, feature_filter, scenario_filter):
        tree.delete(*tree.get_children()) #Limpiar el Treeview antes de insertar datos

        conn = sqlite3.connect("features.db")
        cursor = conn.cursor()

        # Construir la consulta SQL de forma dinámica
        query = "SELECT * FROM Step WHERE 1=1"  # Reemplaza "tu_tabla_principal" con el nombre de tu tabla
        if feature_filter != "":
            query += " AND feature_id IN (SELECT id FROM Feature WHERE name = ?)"
        if scenario_filter != "":
            query += " AND scenario_id IN (SELECT id FROM Scenario WHERE name LIKE ?)"

        # Ejecutar la consulta con los parámetros correctos
        params = tuple(filter(None, [feature_filter, f"%{scenario_filter}%"]))
        cursor.execute(query, params)
        data = cursor.fetchall()
        for item in data:
            tree.insert("", "end", values=item)

        conn.close()
        
    #Llamada a la función para insertar datos inicialmente
    insertar_datos(tree, features, scenarios, steps)

    #Ajustar ancho de las columnas
    for col in tree['columns']:
        widths = [font.Font().measure(tree.set(k, col)) for k in tree.get_children()]
        maxwidth = max(widths)
        tree.column(col, width=maxwidth)

    return tree

# Ejemplo de uso:
# Assuming 'root' is your main window and 'frame' is the frame where you want to display the results
# tree = buscar_features(frame, texts)
