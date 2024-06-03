from flask import Flask
app =Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    # Aquí se manejarán las solicitudes relacionadas con el chat
    return "Hola desde el servidor!"

@app.route('/')
def index():
    return "HolaMundo"


if __name__ == '__main__':
    app.run(debug=True)
