from experta import Fact, Rule, KnowledgeEngine

class Message(Fact):
    pass

class Chatbot(KnowledgeEngine):
    @Rule(Message(content="Hola"))
    def greet(self):
        print("Chatbot: ¡Hola! ¿En qué puedo ayudarte?")

    @Rule(Message(content="Adiós"))
    def farewell(self):
        print("Chatbot: ¡Hasta luego!")

    # Agrega más reglas según sea necesario para manejar diferentes entradas del usuario

# Instanciar el chatbot y cargar las reglas
chatbot = Chatbot()
chatbot.reset()

# Ejemplo de interacción con el chatbot
chatbot.declare(Message(content="Hola"))
chatbot.run()
