import tkinter as tk
from tkinter import ttk
from motor_inferencia import MotorInferencia
from base_conocimiento import descripciones

# Recomendaciones solo para las enfermedades del conjunto de reglas
recomendaciones = {
    "bronquitis aguda": "Se sugiere hidratación, reposo y seguimiento médico si la tos persiste. Evitar humo y contaminantes.",
    "bronquitis crónica": "Evitar exposición al humo de tabaco y contaminantes. Consultar con neumólogo para control prolongado.",
    "asma": "Se recomienda realizar espirometría, usar broncodilatadores si es necesario y evitar alérgenos conocidos.",
    "neumonía": "Requiere radiografía de tórax y evaluación médica inmediata. Puede requerir antibióticos o internación.",
    "epoc": "Consultar con un neumólogo. Posible uso de broncodilatadores y control periódico de oxígeno.",
    "covid-19": "Realizar prueba PCR o antígenos, aislamiento y monitoreo de saturación de oxígeno.",
    "insuficiencia respiratoria aguda": "Acudir a urgencias inmediatamente. Requiere valoración médica y oxigenoterapia.",
    "irritación bronquial por contaminantes": "Evitar exposición a contaminantes, mantener buena ventilación y reposo respiratorio.",
}

class InterfazExperto:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Experto - Diagnóstico Respiratorio")
        self.master.geometry("960x720")
        self.master.configure(bg="#f4f4f4")

        # --- Sección de datos del paciente ---
        tk.Label(master, text="Datos del paciente:", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=8)
        frame_datos = tk.Frame(master, bg="#f4f4f4")
        frame_datos.pack(pady=4, fill="x", padx=12)

        tk.Label(frame_datos, text="Edad:", bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.edad = tk.Entry(frame_datos, width=8)
        self.edad.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        tk.Label(frame_datos, text="Sexo:", bg="#f4f4f4").grid(row=0, column=2, padx=5, pady=4, sticky="e")
        self.sexo = ttk.Combobox(frame_datos, values=["", "Masculino", "Femenino"], width=12)
        self.sexo.grid(row=0, column=3, padx=5, pady=4, sticky="w")

        tk.Label(frame_datos, text="Saturación O₂ (%):", bg="#f4f4f4").grid(row=0, column=4, padx=5, pady=4, sticky="e")
        self.saturacion = tk.Entry(frame_datos, width=8)
        self.saturacion.grid(row=0, column=5, padx=5, pady=4, sticky="w")

        # --- Sección de síntomas ---
        ttk.Label(master, text="Seleccione los síntomas observados:", font=("Arial", 14, "bold"), background="#f4f4f4").pack(pady=10)
        frame_campos = ttk.Frame(master)
        frame_campos.pack(pady=10)

        # Quitamos saturacion_baja del listado de selección manual
        sintomas = [(k, v) for k, v in descripciones.items() if k != "saturacion_baja"]

        self.vars = {}
        columnas = 3
        filas_por_columna = len(sintomas) // columnas + 1

        for i, (clave, texto) in enumerate(sintomas):
            col = i // filas_por_columna
            row = i % filas_por_columna
            var = tk.BooleanVar()
            self.vars[clave] = var
            ttk.Checkbutton(frame_campos, text=texto, variable=var).grid(row=row, column=col, sticky="w", padx=10, pady=3)

        # Botones de acción
        frame_botones = tk.Frame(master, bg="#f4f4f4")
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Diagnosticar", command=self.diagnosticar).grid(row=0, column=0, padx=8)
        ttk.Button(frame_botones, text="Ver explicación", command=self.mostrar_explicacion).grid(row=0, column=1, padx=8)

        # Resultado
        self.resultado = tk.Text(master, wrap="word", width=110, height=14, font=("Arial", 12))
        self.resultado.pack(pady=15)

        self.motor = None

    def diagnosticar(self):
        hechos = [clave for clave, var in self.vars.items() if var.get()]

        # --- Evaluación automática de edad y saturación ---
        edad_texto = self.edad.get().strip()
        sexo = self.sexo.get()
        saturacion_texto = self.saturacion.get().strip()

        try:
            edad = int(edad_texto)
            if edad >= 60:
                hechos.append("edad")
        except ValueError:
            edad = None

        try:
            saturacion = float(saturacion_texto)
            if saturacion < 93:
                hechos.append("saturacion_baja")
        except ValueError:
            saturacion = None

        self.motor = MotorInferencia(hechos)
        resultados = self.motor.diagnosticar_con_probabilidad()

        resultados_filtrados = [(d, p) for d, p in resultados if p >= 50]

        if not resultados_filtrados:
            texto_diagnostico = "No se pudo determinar un diagnóstico con una certeza superior al 50%."
        else:
            texto_diagnostico = "Diagnóstico(s) presuntivo(s):\n\n"
            for enfermedad, prob in resultados_filtrados:
                recomendacion = recomendaciones.get(enfermedad.lower(), "Sin recomendación específica.")
                texto_diagnostico += f"• {enfermedad} — Certeza: {prob:.1f}%\n"
                texto_diagnostico += f"  ↳ Recomendación: {recomendacion}\n\n"

        texto_final = (
            f"Sexo: {sexo or 'No especificado'} | "
            f"Edad: {edad_texto or 'No especificada'} | "
            f"Saturación: {saturacion_texto or 'No especificada'}\n\n"
            f"{texto_diagnostico}"
        )

        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, texto_final)

    def mostrar_explicacion(self):
        if not self.motor:
            return
        texto = self.motor.explicacion.generar_explicacion()
        ventana = tk.Toplevel(self.master)
        ventana.title("Explicación del diagnóstico")
        ventana.geometry("700x500")
        text_area = tk.Text(ventana, wrap="word", font=("Arial", 11))
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        text_area.insert(tk.END, texto)
        text_area.config(state="disabled")
