from flask import Flask, request, render_template, jsonify
from experta import Fact

app = Flask(__name__)

# Importar la lógica del chatbot
from mi_chatbot import Chatbot, Message, MentalHealthChatbot, Symptom, Emotion, Context, Explanation
from bayesian_model import predict_emotion_and_symptom

# Crear una instancia del chatbot
chatbot = Chatbot()
chatbot_engine = MentalHealthChatbot()
chatbot_engine.reset()

# Variable global para almacenar la información de la última emoción detectada
last_emotion = None

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global last_emotion
    
    if request.method == 'POST':
        data = request.json
        user_input = data.get('message')
        
        # Reseteamos el motor para limpiar cualquier hecho previo
        chatbot_engine.reset()

        # Declaramos los hechos basados en la entrada del usuario
        if 'hola' in user_input.lower():
            chatbot_engine.declare(Message(content='Hola'))
        elif 'adiós' in user_input.lower():
            chatbot_engine.declare(Message(content='Adiós'))        
        else:
            # Identificar la emoción del usuario
            emotions = []

            if 'triste' in user_input.lower():
                emotions.append('triste')
            if 'estresado' in user_input.lower():
                emotions.append('estresado')
            if 'contento' in user_input.lower():
                emotions.append('contento')
            
            for emotion in emotions:
                chatbot_engine.declare(Emotion(state=emotion))
                last_emotion = emotion
        
        chatbot_engine.run()
        
        # Obtener la respuesta del sistema experto
        response_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Fact and 'response' in fact), None)
        explanation_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Explanation), None)

        response = response_fact['response'] if response_fact else None
        explanation = explanation_fact['info'] if explanation_fact else None

        if not response:
            response = "¿Te gustaría saber más sobre esta emoción?"
        
        return jsonify({'response': response, 'explanation': explanation})
    
    return render_template('basic.html')

@app.route('/expand', methods=['POST'])
def expand():
    global last_emotion
    
    if request.method == 'POST':
        data = request.json
        user_input = data.get('message')

        if last_emotion:
            if 'si' in user_input.lower():
                chatbot_engine.reset()
                chatbot_engine.declare(Emotion(state=last_emotion))
                chatbot_engine.declare(Message(content='Expandir'))
                chatbot_engine.run()

                explanation_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Explanation), None)
                explanation = explanation_fact['info'] if explanation_fact else None

                last_emotion = None  # Restablecer last_emotion a None después de manejar la solicitud de expansión

                return jsonify({'response': explanation})

            elif 'no' in user_input.lower():
                last_emotion = None  # Restablecer last_emotion a None si el usuario no quiere ampliar la información
                return jsonify({'response': "Entendido, ¿en qué más puedo ayudarte?"})

        return jsonify({'response': "Lo siento, no entendí tu respuesta."})

if __name__ == '__main__':
    app.run(debug=True)




