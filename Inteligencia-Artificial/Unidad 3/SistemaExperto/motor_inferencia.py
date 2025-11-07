from base_conocimiento import reglas, descripciones
from explicacion import Explicacion

class MotorInferencia:
    def __init__(self, hechos):
        self.hechos = set(hechos)
        self.explicacion = Explicacion()

    def diagnosticar_con_probabilidad(self):
        """
        Calcula la probabilidad de cada diagnóstico según la cantidad de síntomas coincidentes.
        Registra solo los síntomas realmente presentes para la explicación.
        """
        resultados = []

        for condiciones, conclusion in reglas:
            total = len(condiciones)
            coincidencias = [cond for cond in condiciones if cond in self.hechos]
            num_coincidencias = len(coincidencias)
            probabilidad = (num_coincidencias / total) * 100 if total > 0 else 0

            if num_coincidencias > 0:
                sintomas_presentes = [descripciones.get(c, c) for c in coincidencias]
                self.explicacion.registrar_regla(sintomas_presentes, conclusion)
                resultados.append((conclusion.capitalize(), probabilidad))

        # Ordenar de mayor a menor probabilidad
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados
