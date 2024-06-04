import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Definir la estructura de la red
model = BayesianNetwork([
    ('context', 'emotion'),
    ('emotion', 'symptom'),   
])

# Definir las distribuciones de probabilidad condicional (CPDs)
cpd_emotion = TabularCPD(variable='emotion', variable_card=3,
                         values=[[0.354, 0.306],
                                [0.415, 0.225],
                                [0.231, 0.469]],
                         evidence=['context'],  # Aquí se añade 'context' como evidencia
                         evidence_card=[2],  # Se asume que 'context' tiene 2 estados
                         state_names={'emotion': ['contento', 'triste', 'estresado'],
                                      'context': ['problemas_familiares', 'dificultades_en_el_trabajo']})


cpd_symptom = TabularCPD(variable='symptom', variable_card=4,
                         values=[
                             [0.7, 0.2, 0.1],  # sin sintomas
                             [0.1, 0.4, 0.2],  # fatiga
                             [0.1, 0.3, 0.4],  # insomnio
                             [0.1, 0.1, 0.3]   # ansiedad
                         ],
                         evidence=['emotion'],
                         evidence_card=[3],
                         state_names={'symptom': ['sin sintomas', 'fatiga', 'insomnio', 'ansiedad'],
                                      'emotion': ['contento', 'triste', 'estresado'],
                                      'context': ['problemas_familiares', 'dificultades_en_el_trabajo']})

cpd_context = TabularCPD(variable='context', variable_card=2,
                         values=[[0.8], [0.2]],
                         state_names={'context': ['problemas_familiares', 'dificultades_en_el_trabajo']})

# Agregar CPDs al modelo
model.add_cpds(cpd_emotion, cpd_symptom ,cpd_context)

# Validar el modelo
model.check_model()

# Crear el objeto de inferencia fuera de la función para que esté disponible globalmente
inference = VariableElimination(model)

# Función para predecir el estado emocional y el síntoma
def predict_emotion_and_symptom(emotion_state, context_situation):
    query_result = inference.map_query(variables=['symptom'], evidence={'emotion': emotion_state, 'context': context_situation })
    most_probable_symptom = query_result['symptom']
    return emotion_state, most_probable_symptom,context_situation

 

