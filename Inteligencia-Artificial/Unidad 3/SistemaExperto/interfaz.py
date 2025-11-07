# interfaz.py
# Interfaz gráfica del sistema experto (actualizada: más campos y mejor distribución)

import tkinter as tk
from tkinter import ttk
from motor_inferencia import MotorInferencia


class InterfazGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema Experto - Diagnóstico Respiratorio")
        master.geometry("1000x820")  # más ancho para varias columnas
        master.resizable(False, False)

        # --- Datos demográficos --- 
        tk.Label(master, text="Datos del paciente:", font=("Arial", 12, "bold")).pack(pady=8)
        frame_datos = tk.Frame(master)
        frame_datos.pack(pady=4, fill="x", padx=12)

        tk.Label(frame_datos, text="Edad:").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.edad = tk.Entry(frame_datos, width=8)
        self.edad.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        tk.Label(frame_datos, text="Sexo:").grid(row=0, column=2, padx=5, pady=4, sticky="e")
        self.sexo = ttk.Combobox(frame_datos, values=["", "Masculino", "Femenino"], width=12)
        self.sexo.grid(row=0, column=3, padx=5, pady=4, sticky="w")

        tk.Label(frame_datos, text="Saturación O₂ (%):").grid(row=0, column=4, padx=5, pady=4, sticky="e")
        self.saturacion = tk.Entry(frame_datos, width=8)
        self.saturacion.grid(row=0, column=5, padx=5, pady=4, sticky="w")

        # --- Síntomas y signos (grid con varias columnas) ---
        tk.Label(master, text="Seleccione los síntomas / signos / factores de riesgo presentes:",
                 font=("Arial", 12, "bold")).pack(pady=8)

        frame_sintomas = ttk.Frame(master)
        frame_sintomas.pack(padx=12, pady=4, fill="x")

        # Lista ampliada de campos (incluye los nuevos que mencionaste)
        self.campos = {
            "tos": "Tos",
            "tos_productiva": "Tos con flema",
            "tos_nocturna_o_ejercicio": "Tos nocturna o por ejercicio",
            "duracion_sintomas_menor_3_semanas": "Síntomas < 3 semanas",
            "dificultad_respiratoria": "Dificultad para respirar",
            "disnea_cronica": "Falta de aire prolongada",
            "sibilancias": "Sibilancias (silbido al respirar)",
            "crepitantes": "Crepitantes en auscultación",
            "dolor_pecho": "Dolor en el pecho",
            "fiebre": "Fiebre",
            "fatiga": "Fatiga o cansancio",
            "anosmia": "Pérdida del olfato",
            "infeccion_respiratoria_previa": "Infección respiratoria previa",
            "rx_consolidacion": "Consolidación pulmonar en Rx",
            "tabaquismo": "Fumador (tabaquismo)",
            "antecedente_epoc": "Antecedente de EPOC",
            "antecedentes_alergia": "Alergias o asma previa",
            "exposicion_contaminantes": "Exposición a contaminantes"
        }

        self.vars = {}
        columnas = 3
        i = 0
        for key, text in self.campos.items():
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(frame_sintomas, text=text, variable=var)
            # distribuir en grid
            chk.grid(row=i // columnas, column=i % columnas, sticky="w", padx=18, pady=6)
            self.vars[key] = var
            i += 1

        # --- Botones ---
        frame_botones = tk.Frame(master)
        frame_botones.pack(pady=12)

        tk.Button(frame_botones, text="Evaluar diagnóstico",
                  font=("Arial", 12, "bold"),
                  bg="#0078D7", fg="white",
                  command=self.ejecutar_sistema
                  ).grid(row=0, column=0, padx=10)

        tk.Button(frame_botones, text="Limpiar",
                  font=("Arial", 11),
                  command=self.resetear_formulario
                  ).grid(row=0, column=1, padx=10)

        # --- Área de resultado (más grande) ---
        tk.Label(master, text="Resultado del diagnóstico:", font=("Arial", 12, "bold")).pack(pady=6)
        # Hacemos la caja más grande para que quepa toda la explicación
        self.resultado = tk.Text(master, height=20, width=115, wrap="word", bg="#F8F8F8", font=("Arial", 10))
        self.resultado.pack(padx=12, pady=6)

        # etiqueta de nota/recomendación corta
        self.nota = tk.Label(master, text="", font=("Arial", 10), fg="gray")
        self.nota.pack(pady=4)

    def ejecutar_sistema(self):
        # Recolectar datos desde los checkboxes
        datos = {k: v.get() for k, v in self.vars.items()}

        # Procesar saturación (saturacion_baja)
        try:
            sat = float(self.saturacion.get())
            datos["saturacion_baja"] = True if sat < 93 else False
        except Exception:
            datos["saturacion_baja"] = False

        # Edad avanzada si >= 65
        try:
            edad_val = int(self.edad.get())
            datos["edad"] = True if edad_val >= 65 else False
        except Exception:
            datos["edad"] = False

        # Sexo (normalizado)
        sexo_val = self.sexo.get().strip()
        datos["sexo"] = sexo_val.lower() if sexo_val else ""

        # Llamar al motor de inferencia
        motor = MotorInferencia(datos)
        diagnosticos = motor.evaluar()

        # Mostrar resultado
        self.resultado.delete(1.0, tk.END)
        self.nota.config(text="")

        if not diagnosticos:
            self.resultado.insert(tk.END, "❌ No se pudo determinar un diagnóstico con la información ingresada.\n")
            self.resultado.insert(tk.END, "\nSugerencias:\n - Añade más signos/síntomas relevantes.\n - Completa edad y saturación si están disponibles.\n")
            self.nota.config(text="El sistema necesita evidencia suficiente para sugerir un diagnóstico.")
            return

        # Imprimir diagnósticos (pueden ser varios)
        for idx, diag in enumerate(diagnosticos, start=1):
            evidencias_texto = ", ".join(diag["evidencias"]) if diag["evidencias"] else "No hay evidencias registradas"
            self.resultado.insert(
                tk.END,
                f"{idx}. ✅ Diagnóstico sugerido: {diag['diagnostico']}\n"
                f"    • Nivel de confianza: {diag['certeza']*100:.0f}%\n"
                f"    • Evidencias clínicas: {evidencias_texto}.\n"
                f"    • Recomendación: {diag.get('recomendacion', 'Consulte con un profesional de salud.')}\n\n"
            )

        self.nota.config(text=f"{len(diagnosticos)} diagnóstico(s) sugerido(s).")

    def resetear_formulario(self):
        # limpiar campos demográficos
        self.edad.delete(0, tk.END)
        self.sexo.set("")
        self.saturacion.delete(0, tk.END)
        # limpiar checkboxes
        for var in self.vars.values():
            var.set(False)
        # limpiar resultado
        self.resultado.delete(1.0, tk.END)
        self.nota.config(text="")

def iniciar_gui():
    root = tk.Tk()
    app = InterfazGUI(root)
    root.mainloop()
