import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def buscar_features_editable(frame, texts):
    """Busca y muestra features en un Treeview editable con filtros.

    Args:
        frame (tk.Frame): Frame donde se mostrará el Treeview.
        texts (dict): Diccionario con textos para la interfaz.
    """
    # Limpiar la ventana
    for widget in frame.winfo_children():
        widget.destroy()

    # Conexión inicial a la base de datos
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()

    # Obtener datos iniciales
    cursor.execute("SELECT id, name FROM Feature")
    features = cursor.fetchall()
    cursor.execute("SELECT id, name, feature_id FROM Scenario")
    scenarios = cursor.fetchall()
    conn.close()

    # Variables para los combos
    feature_var = tk.StringVar()
    scenario_var = tk.StringVar()

    # Crear combobox para filtrar
    ttk.Label(frame, text=texts["feature"]).grid(row=0, column=0, sticky=tk.W)
    feature_combobox = ttk.Combobox(frame, textvariable=feature_var, state="readonly", width=30)
    feature_combobox['values'] = [feature[1] for feature in features]
    feature_combobox.grid(row=0, column=1, sticky=tk.W)

    ttk.Label(frame, text=texts["scenario"]).grid(row=0, column=2, sticky=tk.W)
    scenario_combobox = ttk.Combobox(frame, textvariable=scenario_var, state="readonly", width=30)
    scenario_combobox.grid(row=0, column=3, sticky=tk.W)

    # Crear Treeview
    tree = ttk.Treeview(frame, columns=("Feature", "Scenario", "Keyword", "Step"), show="headings")
    tree.heading("Feature", text=texts["feature"])
    tree.heading("Scenario", text=texts["scenario"])
    tree.heading("Keyword", text=texts["keyword"])
    tree.heading("Step", text=texts["step"])
    tree.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)

    # Configurar estilos
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="blue")

    # Función para cargar datos al Treeview
    def load_tree_data(feature_id=None, scenario_id=None):
        conn = sqlite3.connect("features.db")
        cursor = conn.cursor()

        # Construir consulta SQL basada en los filtros
        query = """
        SELECT Step.id, Feature.name, Scenario.name, Step.keyword, Step.text
        FROM Step
        JOIN Scenario ON Step.scenario_id = Scenario.id
        JOIN Feature ON Scenario.feature_id = Feature.id
        """
        params = []
        if feature_id:
            query += " WHERE Feature.id = ?"
            params.append(feature_id)
        if scenario_id:
            query += " AND Scenario.id = ?" if feature_id else " WHERE Scenario.id = ?"
            params.append(scenario_id)

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        # Limpiar Treeview y rellenarlo con datos
        tree.delete(*tree.get_children())
        for row in data:
            tree.insert("", "end", iid=row[0], values=row[1:])

    # Cargar datos iniciales en el Treeview
    load_tree_data()

    # Función para manejar cambios en los combos
    def on_combo_change(event=None):
        feature_name = feature_var.get()
        scenario_name = scenario_var.get()

        # Obtener ID de la feature seleccionada
        feature_id = next((f[0] for f in features if f[1] == feature_name), None)
        scenario_id = None

        if feature_id:
            # Filtrar escenarios según la feature seleccionada
            filtered_scenarios = [s for s in scenarios if s[2] == feature_id]
            scenario_combobox['values'] = [s[1] for s in filtered_scenarios]
            scenario_combobox.set("")
        else:
            scenario_combobox['values'] = []

        if scenario_name:
            scenario_id = next((s[0] for s in scenarios if s[1] == scenario_name), None)

        # Actualizar Treeview
        load_tree_data(feature_id, scenario_id)

    # Asociar los combos al evento de cambio
    feature_combobox.bind("<<ComboboxSelected>>", on_combo_change)
    scenario_combobox.bind("<<ComboboxSelected>>", on_combo_change)

    # Función para manejar edición
    def start_edit(event):
        region = tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        column_id = tree.identify_column(event.x)
        row_id = tree.identify_row(event.y)
        if not row_id or column_id == "#0":
            return

        column_index = int(column_id[1:]) - 1
        current_value = tree.item(row_id, "values")[column_index]

        # Obtener posición y tamaño de la celda
        bbox = tree.bbox(row_id, column_id)
        if not bbox:
            return

        # Crear Entry para edición
        entry = tk.Entry(tree, justify="center")
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        entry.insert(0, current_value)
        entry.focus()

        def save_edit(event=None):
            new_value = entry.get()
            if not new_value.strip():
                messagebox.showwarning("Advertencia", "El valor no puede estar vacío.")
                cancel_edit()
                return

            # Actualizar Treeview
            values = list(tree.item(row_id, "values"))
            values[column_index] = new_value
            tree.item(row_id, values=values)

            # Actualizar base de datos
            update_database(int(row_id), column_index, new_value)

            entry.destroy()

        def cancel_edit(event=None):
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", cancel_edit)

    def update_database(row_id, column_index, new_value):
        """
        Actualiza la base de datos con el valor editado.
        
        Args:
            row_id (int): ID del Step editado.
            column_index (int): Índice de la columna editada.
            new_value (str): Nuevo valor ingresado.
        """
        try:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()

            if column_index == 2:  # Editar Step.keyword
                cursor.execute("UPDATE Step SET keyword = ? WHERE id = ?", (new_value, row_id))
            elif column_index == 3:  # Editar Step.text
                cursor.execute("UPDATE Step SET text = ? WHERE id = ?", (new_value, row_id))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar la base de datos: {e}")

    # Asociar doble clic para editar
    tree.bind("<Double-1>", start_edit)

    # Ajustar ancho de columnas
    for col in tree["columns"]:
        tree.column(col, width=150)

    return tree
