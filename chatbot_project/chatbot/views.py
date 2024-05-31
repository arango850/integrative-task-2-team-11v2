from django.shortcuts import render

# Create your views here.
# chatbot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
from .models import Conversation
from .serializers import ConversationSerializer

# Cargar el modelo y el tokenizador entrenados
model = BertForSequenceClassification.from_pretrained('saved_model')
tokenizer = BertTokenizer.from_pretrained('saved_model')

# Asegurarse de que el modelo esté en modo evaluación
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

label_encoder = ...  # Cargar o definir tu codificador de etiquetas

max_len = 128

def predict_intent(text):
    encoded_dict = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=max_len,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
    )
    
    input_ids = encoded_dict['input_ids'].to(device)
    attention_mask = encoded_dict['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, token_type_ids=None, attention_mask=attention_mask)
    
    logits = outputs[0]
    logits = logits.detach().cpu().numpy()
    probabilities = torch.nn.functional.softmax(torch.tensor(logits), dim=1).numpy()
    predicted_label_idx = np.argmax(probabilities, axis=1).flatten()
    predicted_label = label_encoder.inverse_transform(predicted_label_idx)[0]
    
    return predicted_label, probabilities[0][predicted_label_idx]

class PredictIntentView(APIView):
    def post(self, request):
        message = request.data.get('message')
        user_id = request.data.get('user_id')
        predicted_label, probability = predict_intent(message)

        conversation = Conversation(
            user_id=user_id,
            message=message,
            response=predicted_label
        )
        conversation.save()

        response = {
            'intent': predicted_label,
            'probability': float(probability)
        }
        return Response(response, status=status.HTTP_200_OK)


