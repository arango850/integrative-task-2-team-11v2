from flask import Flask, request, render_template, jsonify
from experta import Fact

app = Flask(__name__)

# Importar la lógica del chatbot
from mi_chatbot import Chatbot, Message, MentalHealthChatbot, Symptom, Emotion, Context
from bayesian_model import predict_emotion_and_symptom

# Crear una instancia del chatbot
chatbot = Chatbot()
chatbot_engine = MentalHealthChatbot()
chatbot_engine.reset()

@app.route('/chat', methods=['GET', 'POST'])
def chat():
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
            # Identificar los problemas de salud mental
            symptoms = []
            emotions = []
            contexts = []

            if 'ansiedad' in user_input.lower():
                symptoms.append('ansiedad')
            if 'depresion' in user_input.lower():
                symptoms.append('depresion')
            if 'fatiga' in user_input.lower():
                symptoms.append('fatiga')
            if 'insomnio' in user_input.lower():
                symptoms.append('insomnio')
            
            if 'triste' in user_input.lower():
                emotions.append('triste')
            if 'estresado' in user_input.lower():
                emotions.append('estresado')
            if 'contento' in user_input.lower():
                emotions.append('contento')
            
            if 'problemas familiares' in user_input.lower():
                contexts.append('problemas_familiares')
            if 'dificultades en el trabajo' in user_input.lower():
                contexts.append('dificultades_en_el_trabajo')
            
            for symptom in symptoms:
                chatbot_engine.declare(Symptom(type=symptom))
            for emotion in emotions:
                chatbot_engine.declare(Emotion(state=emotion))
            for context in contexts:
                chatbot_engine.declare(Context(situation=context))
        
        chatbot_engine.run()
        
        response_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Fact and 'response' in fact), None)
        
        response = response_fact['response'] if response_fact else "No estoy seguro de cómo responder a eso."
        
        return jsonify({'response': response})
    
    return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)


