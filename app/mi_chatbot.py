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

class Saludos(Fact):
    pass

class Symptom(Fact):
    pass

class Emotion(Fact):
    pass

class Context(Fact):
    pass

class MentalHealthChatbot(KnowledgeEngine):
    @Rule(Symptom(type='ansiedad'))
    def handle_anxiety(self):
        self.declare(Fact(response="Parece que estás experimentando ansiedad. Aquí hay algunos ejercicios de respiración que podrían ayudarte a relajarte."))

    @Rule(Symptom(type='depresion'))
    def handle_depression(self):
        self.declare(Fact(response="La depresión puede ser muy difícil. Hablar con un profesional de salud mental puede ser muy útil. ¿Te gustaría saber más sobre cómo encontrar uno?"))

    @Rule(Emotion(state='triste'))
    def handle_sadness(self):
        self.declare(Fact(response="Siento que te sientes triste. Hablar sobre tus sentimientos con alguien de confianza puede ser muy útil."))

    @Rule(Emotion(state='estresado'))
    def handle_stress(self):
        self.declare(Fact(response="El estrés puede ser abrumador. Tomar un descanso y hacer algo que disfrutes puede ayudar."))

    @Rule(Context(situation='problemas_familiares'))
    def handle_family_problems(self):
        self.declare(Fact(response="Los problemas familiares pueden ser muy estresantes. Hablar con un consejero familiar puede ser beneficioso."))

    @Rule(Emotion(state='contento'))
    def handle_happiness(self):
        self.declare(Fact(response="¡Es genial escuchar que te sientes contento! Mantener prácticas que te hagan sentir bien es importante."))

    @Rule(Symptom(type='insomnio'))
    def handle_insomnia(self):
        self.declare(Fact(response="El insomnio puede ser muy difícil de manejar. Establecer una rutina de sueño y evitar la cafeína antes de dormir puede ayudar. Si el problema persiste, considera hablar con un profesional de salud."))

    @Rule(Symptom(type='fatiga'))
    def handle_fatigue(self):
        self.declare(Fact(response="La fatiga puede tener muchas causas. Asegúrate de estar durmiendo lo suficiente y de llevar una dieta balanceada. Si la fatiga persiste, consulta a un médico."))

    @Rule(Context(situation='dificultades_en_el_trabajo'))
    def handle_work_issues(self):
        self.declare(Fact(response="Las dificultades en el trabajo pueden ser muy estresantes. Intentar establecer límites claros entre el trabajo y la vida personal puede ayudar a manejar el estrés laboral."))

    @Rule(Message(content="Hola"))
    def greet(self):
         self.declare(Fact(response="¡Hola! ¿En qué puedo ayudarte?"))

    @Rule(Message(content="Adiós"))
    def farewell(self):
        self.declare(Fact(response="¡Hasta luego!"))   

# Instanciar el chatbot y cargar las reglas
chatbot = Chatbot()
chatbot.reset()

# Ejemplo de interacción con el chatbot
chatbot.declare(Message(content="Hola"))
chatbot.run()


