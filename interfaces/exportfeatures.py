import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3


def export_feature(frame, texts):
    """Función para exportar las features seleccionadas a un archivo JSON."""
    
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Mantener la conexión abierta mientras sea necesario
    conn = sqlite3.connect("features.db")
    cursor = conn.cursor()

    try:
        # Obtener todas las features de la base de datos
        cursor.execute("SELECT * FROM Feature")
        features = cursor.fetchall()

        # Verificamos si hay datos para mostrar
        if not features:
            messagebox.showwarning(texts["warning"], texts["no_features"])
            return

        # Crear el título de la sección (parametrizable)
        title_label = tk.Label(frame, text=texts["export_title"], font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Crear el combobox con las features disponibles
        feature_names = [feature[1] for feature in features]  # Suponiendo que el nombre está en la columna 1
        feature_combobox = ttk.Combobox(frame, values=feature_names, state="readonly", width=40)
        feature_combobox.grid(row=1, column=0, columnspan=2, pady=10)

        # Función para exportar la feature seleccionada
        def on_export():
            # Obtener el nombre de la feature seleccionada
            selected_feature_name = feature_combobox.get()

            if not selected_feature_name:
                messagebox.showwarning(texts["warning"], texts["select_feature"])
                return

            # Conectar a la base de datos
            conn = sqlite3.connect("features.db")
            cursor = conn.cursor()

            try:
                # Obtener la feature seleccionada por nombre
                cursor.execute("SELECT * FROM Feature WHERE name = ?", (selected_feature_name,))
                selected_feature = cursor.fetchone()

                if selected_feature:
                    # Crear el contenido para el archivo .feature
                    feature_name = selected_feature[1]  # Asumiendo que el nombre está en la segunda columna
                    description = selected_feature[2]  # Descripción en la tercera columna (ajustar si es necesario)

                    # Formato básico de un archivo .feature
                    feature_content = f"Feature: {feature_name}\n\n"
                    if description:
                        feature_content += f"  {description}\n\n"
                    
                    # Obtener los escenarios de esta feature
                    cursor.execute("SELECT * FROM Scenario WHERE feature_id = ?", (selected_feature[0],))
                    scenarios = cursor.fetchall()

                    for scenario in scenarios:
                        scenario_name = scenario[2]  # Suponiendo que el nombre del escenario está en la tercera columna
                        feature_content += f"  Scenario: {scenario_name}\n"

                        # Obtener los pasos asociados al escenario
                        cursor.execute("SELECT * FROM Step WHERE scenario_id = ?", (scenario[0],))
                        steps = cursor.fetchall()

                        for step in steps:
                            keyword = step[2]  # Palabra clave (Given, When, Then) en la tercera columna
                            step_text = step[3]  # Texto del paso en la cuarta columna
                            feature_content += f"    {keyword} {step_text}\n"

                    # Especificar el archivo de salida
                    file_name = f"feature_{selected_feature_name}.feature"

                    # Guardar el contenido en un archivo .feature
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(feature_content)

                    # Mensaje de confirmación
                    messagebox.showinfo(texts["export_success"], texts["export_message"].format(file_name))

                else:
                    messagebox.showwarning(texts["warning"], texts["feature_not_found"])

            except sqlite3.Error as e:
                messagebox.showerror(texts["error"], f"Error al exportar: {str(e)}")

            finally:
                conn.close()

        # Crear el botón de exportar
        export_button = tk.Button(frame, text=texts["export_button"], command=on_export)
        export_button.grid(row=2, column=0, columnspan=2, pady=10)

    except sqlite3.Error as e:
        messagebox.showerror(texts["error"], f"Error al conectar con la base de datos: {str(e)}")

    # Aquí cerramos la conexión solo cuando hayamos terminado todo el flujo
    finally:
        # Asegurarnos de cerrar la conexión solo después de todo el proceso.
        conn.close()
