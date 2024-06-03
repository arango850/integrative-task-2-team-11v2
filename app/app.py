from flask import Flask, request, render_template

app = Flask(__name__)

# Importar la lógica del chatbot
from mi_chatbot import Chatbot, Message

# Crear una instancia del chatbot
chatbot = Chatbot()

@app.route('/chat', methods=['GET', 'POST'])
def chat():
     if request.method == 'POST':
        data = request.json
        message_content = data['message']
    # Declarar el mensaje del usuario y ejecutar el chatbot
        chatbot.reset()
        chatbot.declare(Message(content=message_content))
        chatbot.run()
        return "Mensaje del usuario procesado por el chatbot"
     else:
         return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)