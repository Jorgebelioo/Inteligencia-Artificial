import numpy as np
np.product = np.prod  # alias para compatibilidad
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Definir la estructura de la red bayesiana
modelo = BayesianNetwork([
    ('PreferenciaCliente', 'PlatoRecomendado'),
    ('RestriccionDietetica', 'PlatoRecomendado'),
    ('DisponibilidadIngredientes', 'PlatoRecomendado')
])

# CPD para Preferencia del cliente
cpd_preferencia = TabularCPD(
    variable='PreferenciaCliente',
    variable_card=3,
    values=[[0.4], [0.35], [0.25]],
    state_names={'PreferenciaCliente': ['Saludable', 'Italiana', 'Picante']}
)

# CPD para Restricción dietética
cpd_restriccion = TabularCPD(
    variable='RestriccionDietetica',
    variable_card=3,
    values=[[0.5], [0.3], [0.2]],
    state_names={'RestriccionDietetica': ['Ninguna', 'Vegetariana', 'Vegana']}
)

# CPD para Disponibilidad de ingredientes
cpd_disponibilidad = TabularCPD(
    variable='DisponibilidadIngredientes',
    variable_card=2,
    values=[[0.8], [0.2]],
    state_names={'DisponibilidadIngredientes': ['Disponible', 'NoDisponible']}
)

# CPD para el plato recomendado
cpd_plato = TabularCPD(
    variable='PlatoRecomendado',
    variable_card=6,
    values=[
        # Ensalada César
        [0.7,0.6,0.1,0.1,0.1,0.0,0.1,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        # Ensalada Vegana
        [0.1,0.2,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        # Pasta Alfredo
        [0.1,0.1,0.6,0.3,0.2,0.1,0.4,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        # Pasta con Pollo
        [0.05,0.05,0.2,0.4,0.3,0.2,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        # Tacos Picantes
        [0.05,0.05,0.1,0.1,0.3,0.2,0.2,0.3,0.5,0.6,0.7,0.8,0.4,0.3,0.2,0.2,0.1,0.2],
        # Tacos Veganos
        [0.0,0.0,0.0,0.1,0.1,0.0,0.0,0.0,0.5,0.4,0.3,0.2,0.6,0.7,0.8,0.8,0.9,0.8]
    ],
    evidence=['PreferenciaCliente', 'RestriccionDietetica', 'DisponibilidadIngredientes'],
    evidence_card=[3,3,2],
    state_names={
        'PlatoRecomendado':['Ensalada César','Ensalada Vegana','Pasta Alfredo','Pasta con Pollo','Tacos Picantes','Tacos Veganos'],
        'PreferenciaCliente':['Saludable','Italiana','Picante'],
        'RestriccionDietetica':['Ninguna','Vegetariana','Vegana'],
        'DisponibilidadIngredientes':['Disponible','NoDisponible']
    }
)
# Agregar las CPDs al modelo
modelo.add_cpds(cpd_preferencia, cpd_restriccion, cpd_disponibilidad, cpd_plato)

# Verificar consistencia del modelo
print("¿El modelo es válido?", modelo.check_model())

# Inferencia probabilística
inferencia = VariableElimination(modelo)
resultado = inferencia.map_query(
    variables=['PlatoRecomendado'],
    evidence={'PreferenciaCliente': 'Italiana', 'RestriccionDietetica': 'Vegetariana', 'DisponibilidadIngredientes': 'Disponible'}
)


def recommend(evidence_dict):
    """
    Función principal que utiliza la red bayesiana para recomendar un plato.
    Esta es la que el backend FastAPI llamará directamente.
    """
    try:
        q = recommend_example(evidence_dict)
        # Convierte la distribución a un diccionario legible
        resultados = dict(zip(q.state_names['PlatoRecomendado'], q.values))
        recomendado = max(resultados, key=resultados.get)
        return {"PlatoRecomendado": recomendado, "Distribucion": resultados}
    except Exception as e:
        return {"error": str(e)}


def recommend_example(evidence_dict):
    """
    Recibe un diccionario con evidencias (por ejemplo desde la API)
    y devuelve la distribución de probabilidad sobre los platos recomendados.
    """
    evidencia = {}

    # Mapeamos los enteros 0/1 a los estados del modelo
    evidencia['PreferenciaCliente'] = 'Picante' if evidence_dict.get('LikesSpicy') == 1 else 'Italiana'
    evidencia['RestriccionDietetica'] = 'Vegana' if evidence_dict.get('IsVeganCustomer') == 1 else 'Ninguna'
    evidencia['DisponibilidadIngredientes'] = 'Disponible' if evidence_dict.get('IngredientsAvailable') == 1 else 'NoDisponible'


    # Ejecutar inferencia
    inferencia = VariableElimination(modelo)
    q = inferencia.query(variables=['PlatoRecomendado'], evidence=evidencia)

    return q

    
print("Plato recomendado:", resultado['PlatoRecomendado'])
