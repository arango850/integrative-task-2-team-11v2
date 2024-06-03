from flask import Flask, request, render_template, jsonify
from experta import Fact

app = Flask(__name__)

# Importar la lógica del chatbot
from mi_chatbot import Chatbot, Message, MentalHealthChatbot, Symptom, Emotion, Context

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
            if 'ansiedad' in user_input.lower():
                chatbot_engine.declare(Symptom(type='ansiedad'))
            if 'depresion' in user_input.lower():
                chatbot_engine.declare(Symptom(type='depresion'))
            if 'triste' in user_input.lower():
                chatbot_engine.declare(Emotion(state='triste'))
            if 'estresado' in user_input.lower():
                chatbot_engine.declare(Emotion(state='estresado'))
            if 'problemas familiares' in user_input.lower():
                chatbot_engine.declare(Context(situation='problemas_familiares'))
            if 'dificultades en el trabajo' in user_input.lower():
                chatbot_engine.declare(Context(situation='dificultades_en_el_trabajo'))
            if 'contento' in user_input.lower():
                chatbot_engine.declare(Emotion(state='contento'))
            if 'insomnio' in user_input.lower():
                chatbot_engine.declare(Symptom(type='insomnio'))
            if 'fatiga' in user_input.lower():
                chatbot_engine.declare(Symptom(type='fatiga'))

        chatbot_engine.run()

        # Obtener la respuesta generada
        response = "Lo siento, no estoy seguro de cómo ayudarte con eso. ¿Puedes darme más detalles?"
        for fact in chatbot_engine.facts.values():
            if 'response' in fact:
                response = fact['response']
                break

        return jsonify({'response': response})
    else:
        return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)
