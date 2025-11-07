# motor_inferencia.py
# Motor de inferencia

from base_conocimiento import reglas

# Traducciones a lenguaje natural
descripciones = {
    "tos": "tos",
    "tos_productiva": "tos con flema",
    "tos_nocturna_o_ejercicio": "tos nocturna o por ejercicio",
    "dificultad_respiratoria": "dificultad para respirar",
    "sibilancias": "sibilancias (silbido al respirar)",
    "dolor_pecho": "dolor en el pecho",
    "fiebre": "fiebre",
    "anosmia": "pérdida del olfato",
    "tabaquismo": "tabaquismo",
    "antecedente_epoc": "antecedente de EPOC",
    "antecedentes_alergia": "antecedente de alergias o asma",
    "crepitantes": "crepitantes al auscultar los pulmones",
    "disnea_cronica": "falta de aire prolongada",
    "infeccion_respiratoria_previa": "infección respiratoria reciente",
    "rx_consolidacion": "consolidación pulmonar en radiografía",
    "duracion_sintomas_menor_3_semanas": "síntomas de corta duración (menos de 3 semanas)",
    "fatiga": "fatiga o cansancio general",
    "exposicion_contaminantes": "exposición a contaminantes",
    "edad": "edad avanzada",
    "sexo": "sexo",
    "saturacion_baja": "saturación de oxígeno baja (< 93%)"
}

# Recomendaciones según diagnóstico
recomendaciones = {
    "Asma": "Se recomienda realizar una espirometría y evitar alérgenos conocidos.",
    "Neumonía": "Se recomienda radiografía de tórax y evaluación médica inmediata.",
    "Bronquitis aguda": "Se sugiere hidratación, reposo y seguimiento médico si persiste la tos.",
    "EPOC (Exacerbación)": "Consultar con un neumólogo, posible uso de broncodilatadores y control de oxígeno.",
    "COVID-19": "Realizar prueba PCR o antígenos, aislamiento y monitoreo de saturación."
}


class MotorInferencia:
    def __init__(self, hechos_usuario):
        self.hechos = hechos_usuario
        self.diagnosticos = []

    def evaluar(self):
        self.diagnosticos.clear()

        for regla in reglas:
            cumple = True
            evidencias = []

            for condicion, valor in regla["condiciones"]:
                if condicion in self.hechos and self.hechos[condicion] == valor:
                    evidencias.append(descripciones.get(condicion, condicion))
                else:
                    cumple = False
                    break

            if cumple:
                diag = regla["diagnostico"]
                self.diagnosticos.append({
                    "diagnostico": diag,
                    "certeza": regla["factor_certeza"],
                    "evidencias": evidencias,
                    "regla": regla["id"],
                    "recomendacion": recomendaciones.get(diag, "Se recomienda valoración médica.")
                })

        return self.diagnosticos
