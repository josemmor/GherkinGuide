# feature_creator.py
import tkinter as tk
from tkinter import ttk, StringVar
import sqlite3
from tkinter import messagebox
from interfaces.AppManager import AppManager


class FeatureCreator:
    def __init__(self, frame, texts):
        
        self.frame = frame
        self.texts = texts
        self.feature_name_var = StringVar()
        self.description_var = StringVar()
        self.scenario_name_var = StringVar()
        self.step_keyword_var = StringVar()
        self.step_text_var = StringVar()
        self.selected_feature_var = StringVar()
        self.selected_scenario_var = StringVar()
        self.create_feature_window()

    def create_feature_window(self):           
        # Limpiar el frame antes de agregar nuevos elementos
        AppManager.clear_frame(self.frame)
        
        # Crear la interfaz
        self.create_feature_section()
        self.create_scenario_section()
        self.create_step_section()
        #Falta agregar la parte de guardar

    def create_feature_section(self):
        # Título
        fila = 0
        tk.Label(self.frame, text=self.texts["features"], font=("Helvetica", 14)).grid(row=fila, column=0, sticky="w")
        # Vemos features creadas
        self.feature_combobox = ttk.Combobox(self.frame, textvariable=self.selected_feature_var)
        self.feature_combobox.grid(row=fila, column=1, sticky="w")
        # Asocia el evento <<ComboboxSelected>> con el método para actualizar escenarios
        self.feature_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_scenario_combobox())
        # Campos
        fila = 1
        tk.Label(self.frame, text=self.texts["name"], font=("Helvetica", 10)).grid(row=fila, column=0, sticky="w")
        tk.Entry(self.frame, textvariable=self.feature_name_var).grid(row=fila, column=1, sticky="w")
        tk.Label(self.frame, text=self.texts["description"], font=("Helvetica", 10)).grid(row=fila, column=2, sticky="w")
        tk.Entry(self.frame, textvariable=self.description_var).grid(row=fila, column=3, sticky="w")
        tk.Button(self.frame, text=self.texts["create"] + " " + self.texts["features"],
                command=lambda: self.create_feature()).grid(row=fila, column=4, padx=5, sticky="w")
        self.update_feature_combobox()

    def create_scenario_section(self):        
        #Titulo
        fila=2
        self.frame.grid_rowconfigure(fila, minsize=60)  # Espaciador de 50 píxeles
        tk.Label(self.frame, text=self.texts["scenario"], font=("Helvetica", 14)).grid(row=fila, column=0, sticky="w")
        #Vemos scenarios creados
        #TODO: ojo, esto solo debe cargarse si se selecciona el combo de features
        self.scenario_combobox = ttk.Combobox(self.frame, textvariable=self.selected_scenario_var, state="readonly")
        self.scenario_combobox.grid(row=fila, column=1, sticky="w")
        #Campos
        fila=3
        tk.Entry(self.frame, textvariable=self.scenario_name_var).grid(row=fila, column=0, sticky="w")
        tk.Button(self.frame, text=self.texts["create"]+" "+self.texts["scenario"], command=lambda: self.create_scenario()).grid(row=fila, column=1, padx=5, sticky="w")
        self.update_scenario_combobox()
        

    def create_step_section(self):
        # Título
        fila = 4
        self.frame.grid_rowconfigure(fila, minsize=60)  # Espaciador de 20 píxeles
        tk.Label(self.frame, text=self.texts["step"], font=("Helvetica", 14)).grid(row=fila, column=0, sticky="w")

        # Campo 1: Combobox para "Given", "When", "Then"
        fila = 5
        tk.Label(self.frame, text="Keyword:", font=("Helvetica", 10)).grid(row=fila, column=0, sticky="w")
        self.keyword_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.step_keyword_var,
            values=["Given", "When", "Then"],
            state="readonly",
            width=10
        )
        self.keyword_combobox.grid(row=fila, column=1, sticky="w")
        self.keyword_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_step_combobox())

       
        # Campo 3: Combobox para Steps existentes del mismo Keyword
        fila = 6
        tk.Label(self.frame, text=self.texts["step"] +" "+ self.texts["create"] , font=("Helvetica", 10)).grid(row=fila, column=0, sticky="w")
        self.steps_combobox = ttk.Combobox(self.frame, state="readonly", width=40)
        self.steps_combobox.grid(row=fila, column=1, sticky="w")

        # Campo 4: Entry editable con sugerencias de Steps similares
        fila = 7
        tk.Label(self.frame,  text=self.texts["text"], font=("Helvetica", 10)).grid(row=fila, column=0, sticky="w")
        self.suggestions_entry = tk.Entry(self.frame, width=40)
        self.suggestions_entry.grid(row=fila, column=1, sticky="w")
        self.suggestions_entry.bind("<KeyRelease>", lambda event: self.update_suggestions())

        # Botón para crear el Step
        tk.Button(
            self.frame,
            text=self.texts["create"] + " " + self.texts["step"],
            command=lambda: self.create_step()
        ).grid(row=fila, column=2, padx=5, sticky="w")

        # Seccion de estado
        fila = 8
        self.status_label = tk.Label(self.frame, text="", font=("Helvetica", 10), fg="green")
        self.status_label.grid(row=fila, column=0, columnspan=3, sticky="w")
       
    def create_feature(self):
        name = self.feature_name_var.get()  
        if name:
            try:
                description = self.description_var.get()
                conn = sqlite3.connect("features.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Feature (name, description) VALUES (?, ?)", (name, description))
                conn.commit()
                conn.close()
                self.update_feature_combobox()
                self.feature_name_var.set("")
                self.description_var.set("")
            except:
                messagebox.showerror("Error", "Error al crear la característica.")
        else:
            messagebox.showerror("Error", "El nombre de la característica no puede estar vacío.")

    def create_scenario(self):
        feature_name = self.selected_feature_var.get()
        scenario_name = self.scenario_name_var.get()
        if feature_name and scenario_name:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Feature WHERE name = ?", (feature_name,))
            feature_id = cursor.fetchone()
            if feature_id:
                cursor.execute("INSERT INTO Scenario (feature_id, name) VALUES (?, ?)", (feature_id[0], scenario_name))
                conn.commit()
            conn.close()
            self.update_scenario_combobox()
            self.scenario_name_var.set("")
        else:
            messagebox.showerror("Error", "Debes seleccionar una característica y escribir un nombre para el escenario.")

    def create_step(self):
        scenario_name = self.selected_scenario_var.get()
        keyword = self.step_keyword_var.get()
        text = self.suggestions_entry.get()
        if scenario_name and keyword and text:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()
            # Obtener el ID del Scenario seleccionado
            cursor.execute("SELECT id, feature_id FROM Scenario WHERE name = ?", (scenario_name,))
            scenario_info = cursor.fetchone()
            if scenario_info:
                scenario_id, feature_id = scenario_info
                # Insertar el Step en la base de datos
                cursor.execute("INSERT INTO Step (scenario_id, keyword, text) VALUES (?, ?, ?)",
                            (scenario_id, keyword, text))
                conn.commit()
                # Obtener el nombre de la Feature asociada
                cursor.execute("SELECT name FROM Feature WHERE id = ?", (feature_id,))
                feature_name = cursor.fetchone()[0]
                conn.close()

                # Actualizar la etiqueta de estado
                self.status_label.config(
                    text=f"Step creado correctamente en Feature '{feature_name}' y Scenario '{scenario_name}'", 
                    fg="green"
                )

                # Limpiar los campos
                self.step_keyword_var.set("")
                self.step_text_var.set("")
                self.suggestions_entry.delete(0, tk.END)
            else:
                conn.close()
                messagebox.showerror("Error", "No se pudo encontrar el escenario seleccionado.")
        else:
            messagebox.showerror("Error", f"Debes seleccionar un escenario{scenario_name}, un keyword  {keyword} y escribir el texto del paso {text}.")

    def update_feature_combobox(self):
        conn = sqlite3.connect("features.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Feature ORDER BY name")
        features = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.feature_combobox['values'] = features
        if features:
            self.feature_combobox.current(0)
            # Redimensionar el ancho del combobox
            max_width = max(len(feature) for feature in features) + 1  # +1 para un pequeño margen
            self.feature_combobox.config(width=max_width)
        else:
            self.feature_combobox.config(width=10)  # Ancho por defecto si no hay valores

    def update_scenario_combobox(self):
        feature_name = self.selected_feature_var.get()
        if feature_name:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Feature WHERE name = ?", (feature_name,))
            feature_id = cursor.fetchone()
            if feature_id:
                cursor.execute("SELECT name FROM Scenario WHERE feature_id = ? ORDER BY name", (feature_id[0],))
                scenarios = [row[0] for row in cursor.fetchall()]
                self.scenario_combobox['values'] = scenarios
                if scenarios:
                    self.scenario_combobox.current(0)
                    # Redimensionar el ancho del combobox
                    max_width = max(len(scenario) for scenario in scenarios) + 1
                    self.scenario_combobox.config(width=max_width)
                else:
                    self.scenario_combobox.set("")
                    self.scenario_combobox.config(width=10)  # Ancho por defecto si no hay valores
            conn.close()
        else:
            self.scenario_combobox['values'] = []
            self.scenario_combobox.set("")
            self.scenario_combobox.config(width=10)  # Ancho por defecto si no hay selección

    def update_step_combobox(self):
        keyword = self.step_keyword_var.get()
        if keyword:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()
            # Selecciona solo Steps únicos (texto no repetido)
            cursor.execute("SELECT DISTINCT text FROM Step WHERE keyword = ? ORDER BY text", (keyword,))
            steps = [row[0] for row in cursor.fetchall()]
            conn.close()
            self.steps_combobox['values'] = steps
            if steps:
                self.steps_combobox.current(0)  # Selecciona el primer valor por defecto
            else:
                self.steps_combobox.set("")  # Limpia el combobox si no hay resultados
        else:
            self.steps_combobox['values'] = []
            self.steps_combobox.set("")  # Limpia el combobox si no hay keyword seleccionado


    def update_suggestions(self):
        keyword = self.step_keyword_var.get()
        current_text = self.suggestions_entry.get()  # Texto actual en el campo

        if keyword and current_text:
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()
            # Buscar texto que coincida parcialmente
            cursor.execute(
                "SELECT text FROM Step WHERE keyword = ? AND text LIKE ? ORDER BY text",
                (keyword, f"{current_text}%")  # Coincidencia desde el inicio
            )
            suggestions = [row[0] for row in cursor.fetchall()]
            conn.close()

            if suggestions:
                first_suggestion = suggestions[0]
                # Si la sugerencia comienza con el texto actual, completar el resto
                if first_suggestion.startswith(current_text):
                    # Completa el texto sin sobrescribir lo que el usuario está escribiendo
                    self.suggestions_entry.delete(0, tk.END)
                    self.suggestions_entry.insert(0, first_suggestion)
                    self.suggestions_entry.icursor(len(current_text))  # Coloca el cursor después del texto escrito
            else:
                # Si no hay sugerencias, no hacemos cambios
                pass
        else:
            # Si no hay texto o keyword, no hacemos cambios
            pass


