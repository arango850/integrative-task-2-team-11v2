import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the network structure
model = BayesianNetwork([
    ('context', 'emotion'),
    ('emotion', 'symptom'),   
])

# Define the conditional probability distributions (CPDs)
cpd_emotion = TabularCPD(variable='emotion', variable_card=3,
                         values=[[0.354, 0.306],
                                 [0.415, 0.225],
                                 [0.231, 0.469]],
                         evidence=['context'],  # Here 'context' is added as evidence
                         evidence_card=[2],  # Assuming 'context' has 2 states
                         state_names={'emotion': ['happy', 'sad', 'stressed'],
                                      'context': ['family_problems', 'work_difficulties']})

cpd_symptom = TabularCPD(variable='symptom', variable_card=4,
                         values=[
                             [0.7, 0.2, 0.1],  # no symptoms
                             [0.1, 0.4, 0.2],  # fatigue
                             [0.1, 0.3, 0.4],  # insomnia
                             [0.1, 0.1, 0.3]   # anxiety
                         ],
                         evidence=['emotion'],
                         evidence_card=[3],
                         state_names={'symptom': ['no symptoms', 'fatigue', 'insomnia', 'anxiety'],
                                      'emotion': ['happy', 'sad', 'stressed'],
                                      'context': ['family_problems', 'work_difficulties']})

cpd_context = TabularCPD(variable='context', variable_card=2,
                         values=[[0.8], [0.2]],
                         state_names={'context': ['family_problems', 'work_difficulties']})

# Add CPDs to the model
model.add_cpds(cpd_emotion, cpd_symptom, cpd_context)

# Validate the model
model.check_model()

# Create the inference object outside the function to be available globally
inference = VariableElimination(model)

# Function to predict the emotional state and symptom
def predict_emotion_and_symptom(emotion_state, context_situation):
    query_result = inference.map_query(variables=['symptom'], evidence={'emotion': emotion_state, 'context': context_situation})
    most_probable_symptom = query_result['symptom']
    return emotion_state, most_probable_symptom, context_situation


 

