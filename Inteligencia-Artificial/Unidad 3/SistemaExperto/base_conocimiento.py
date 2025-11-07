# base_conocimiento.py
# Base de conocimiento médica (enfermedades respiratorias)

reglas = [
    {
        "id": "R1",
        "nombre": "Asma",
        "condiciones": [
            ("sibilancias", True),
            ("tos_nocturna_o_ejercicio", True),
            ("antecedentes_alergia", True)
        ],
        "diagnostico": "Asma",
        "factor_certeza": 0.9
    },
    {
        "id": "R2",
        "nombre": "Neumonía",
        "condiciones": [
            ("fiebre", True),
            ("tos_productiva", True),
            ("dificultad_respiratoria", True),
            ("crepitantes", True)
        ],
        "diagnostico": "Neumonía",
        "factor_certeza": 0.85
    },
    {
        "id": "R3",
        "nombre": "Bronquitis aguda",
        "condiciones": [
            ("tos", True),
            ("duracion_sintomas_menor_3_semanas", True),
            ("infeccion_respiratoria_previa", True),
            ("rx_consolidacion", False)
        ],
        "diagnostico": "Bronquitis aguda",
        "factor_certeza": 0.75
    },
    {
        "id": "R4",
        "nombre": "EPOC",
        "condiciones": [
            ("antecedente_epoc", True),
            ("tabaquismo", True),
            ("disnea_cronica", True),
            ("saturacion_baja", True)
        ],
        "diagnostico": "EPOC (Exacerbación)",
        "factor_certeza": 0.8
    },
    {
        "id": "R5",
        "nombre": "COVID-19",
        "condiciones": [
            ("fiebre", True),
            ("tos", True),
            ("anosmia", True),
            ("fatiga", True)
        ],
        "diagnostico": "COVID-19",
        "factor_certeza": 0.9
    }
]
