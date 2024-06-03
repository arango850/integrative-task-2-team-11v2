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
        if 'ansiedad' in user_input.lower():
            chatbot_engine.declare(Symptom(type='ansiedad'))
        elif 'depresion' in user_input.lower():
            chatbot_engine.declare(Symptom(type='depresion'))
        elif 'triste' in user_input.lower():
            chatbot_engine.declare(Emotion(state='triste'))
        elif 'estresado' in user_input.lower():
            chatbot_engine.declare(Emotion(state='estresado'))
        elif 'problemas familiares' in user_input.lower():
            chatbot_engine.declare(Context(situation='problemas_familiares'))
        elif 'dificultades en el trabajo' in user_input.lower():
            chatbot_engine.declare(Context(situation='dificultades_en_el_trabajo'))
        elif 'contento' in user_input.lower():
            chatbot_engine.declare(Emotion(state='contento'))
        elif 'insomnio' in user_input.lower():
            chatbot_engine.declare(Symptom(type='insomnio'))
        elif 'fatiga' in user_input.lower():
            chatbot_engine.declare(Symptom(type='fatiga'))
        else:
            chatbot_engine.declare(Fact(response="Lo siento, no estoy seguro de cómo ayudarte con eso. ¿Puedes darme más detalles?"))

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
