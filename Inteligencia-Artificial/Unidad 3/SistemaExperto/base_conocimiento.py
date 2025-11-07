# base_conocimiento.py

# Descripciones legibles de los síntomas
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
    "exposicion_contaminantes": "exposición a contaminantes"
}

# Base de conocimiento (reglas)
reglas = [
    (["tos", "tos_productiva", "duracion_sintomas_menor_3_semanas"], "bronquitis aguda"),
    (["tos", "tos_productiva", "disnea_cronica", "tabaquismo"], "bronquitis crónica"),
    (["tos_nocturna_o_ejercicio", "sibilancias", "antecedentes_alergia"], "asma"),
    (["fiebre", "crepitantes", "rx_consolidacion", "edad"], "neumonía"),
    (["disnea_cronica", "tabaquismo", "antecedente_epoc"], "EPOC"),
    (["fiebre", "tos", "anosmia", "fatiga"], "COVID-19"),
    (["dificultad_respiratoria", "saturacion_baja"], "insuficiencia respiratoria aguda"),
    (["tos", "exposicion_contaminantes"], "irritación bronquial por contaminantes")
]
