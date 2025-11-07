# explicacion.py
class Explicacion:
    def __init__(self):
        self.trazas = []

    def registrar_regla(self, condiciones, conclusion):
        detalle = {
            "condiciones": condiciones,
            "conclusion": conclusion
        }
        self.trazas.append(detalle)

    def generar_explicacion(self):
        if not self.trazas:
            return "No se activaron reglas durante el diagnóstico."

        texto = "O Explicación del razonamiento del sistema experto:\n\n"
        for i, t in enumerate(self.trazas, 1):
            condiciones = ", ".join(t["condiciones"])
            texto += f"{i}. Se cumplieron los sintomas: {condiciones}\n"
            texto += f"   -> Hay probabilidad de: {t['conclusion'].capitalize()}\n\n"
        return texto
