from experta import Fact, Rule, KnowledgeEngine
from bayesian_model import predict_emotion_and_symptom

class Message(Fact):
    pass

class Explanation(Fact):
    pass

class Chatbot(KnowledgeEngine):
    @Rule(Message(content="Hola"))
    def greet(self):
        self.declare(Fact(response="¡Hola! ¿En qué puedo ayudarte?"))

    @Rule(Message(content="Adiós"))
    def farewell(self):
        self.declare(Fact(response="¡Hasta luego!"))

class Symptom(Fact):
    pass

class Emotion(Fact):
    pass

class Context(Fact):
    pass

class MentalHealthChatbot(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.inference = predict_emotion_and_symptom  # Función de inferencia bayesiana
    
    def infer_respuesta(self, emocion, sintoma, contexto):
        # Convertir las variables emocionales y contextuales a un formato que la función de inferencia pueda utilizar
        emotion_mapping = {0: 'contento', 1: 'triste', 2: 'estresado'}
        symptom_mapping = {0: 'sin sintomas', 1: 'fatiga', 2: 'insomnio', 3: 'ansiedad'}
        contex_mapping = {0: 'dificultades_en_el_trabajo', 1: 'problemas_familiares'}

        emotion_state = emotion_mapping[emocion]
        context_situation = contex_mapping[contexto]
        emotion, symptom, context = self.inference(emotion_state,context_situation)

        if emotion.__eq__("contento"):
            return f"La emoción más probable es {emotion} y el síntoma más probable es {symptom} del contexto sin_contexto"
        else:
            return f"La emoción más probable es {emotion} y el síntoma más probable es {symptom} del contexto {context}"

    @Rule(Symptom(type='ansiedad') & Emotion(state='estresado'))
    def handle_anxiety_and_stress(self):
        self.declare(Fact(response=self.infer_respuesta(2, 3, 0)))

    @Rule(Symptom(type='depresion') & Context(situation='problemas_familiares'))
    def handle_depression_and_family_problems(self):
        self.declare(Fact(response=self.infer_respuesta(1, 1, 0)))

    @Rule(Emotion(state='triste') & ~Symptom(type='depresion'))
    def handle_sadness_without_depression(self):
        self.declare(Fact(response=self.infer_respuesta(1, 0, 0)))

    @Rule(Emotion(state='estresado') & Context(situation='dificultades_en_el_trabajo'))
    def handle_stress_and_work_issues(self):
        self.declare(Fact(response=self.infer_respuesta(2, 0, 1)))

    @Rule(Symptom(type='fatiga') & Emotion(state='triste') & ~Symptom(type='insomnio'))
    def handle_fatigue_and_sadness_without_insomnia(self):
        self.declare(Fact(response=self.infer_respuesta(1, 1, 0)))

    @Rule(Symptom(type='insomnio') & Symptom(type='ansiedad'))
    def handle_insomnia_and_anxiety(self):
        self.declare(Fact(response=self.infer_respuesta(2, 3, 0)))

    @Rule(Symptom(type='fatiga') & Symptom(type='insomnio'))
    def handle_fatigue_and_insomnia(self):
        self.declare(Fact(response=self.infer_respuesta(2, 2, 0)))

    @Rule(Symptom(type='depresion') & Emotion(state='triste') & Context(situation='dificultades_en_el_trabajo'))
    def handle_depression_sadness_work_issues(self):
        self.declare(Fact(response=self.infer_respuesta(1, 1, 1)))

    @Rule(Symptom(type='ansiedad'))
    def handle_anxiety(self):
        self.declare(Fact(response=self.infer_respuesta(2, 3, 0)))

    @Rule(Symptom(type='depresion'))
    def handle_depression(self):
        self.declare(Fact(response=self.infer_respuesta(1, 1, 0)))

    @Rule(Emotion(state='triste'))
    def handle_sadness(self):
        self.declare(Fact(response=self.infer_respuesta(1, 0, 0)))

    @Rule(Emotion(state='estresado'))
    def handle_stress(self):
        self.declare(Fact(response=self.infer_respuesta(2, 0, 0)))

    @Rule(Context(situation='problemas_familiares'))
    def handle_family_problems(self):
        self.declare(Fact(response=self.infer_respuesta(0, 0, 0)))

    @Rule(Emotion(state='contento'))
    def handle_happiness(self):
        self.declare(Fact(response=self.infer_respuesta(0, 0, 0)))

    @Rule(Symptom(type='insomnio'))
    def handle_insomnia(self):
        self.declare(Fact(response=self.infer_respuesta(2, 2, 0)))

    @Rule(Symptom(type='fatiga'))
    def handle_fatigue(self):
        self.declare(Fact(response=self.infer_respuesta(1, 1, 0)))

    @Rule(Context(situation='dificultades_en_el_trabajo'))
    def handle_work_issues(self):
        self.declare(Fact(response=self.infer_respuesta(2, 0, 1)))

    @Rule(Message(content="Hola"))
    def greet(self):
        self.declare(Fact(response="¡Hola! ¿En qué puedo ayudarte?"))

    @Rule(Message(content="Adiós"))
    def farewell(self):
        self.declare(Fact(response="¡Hasta luego!"))

    @Rule(Symptom(type='ansiedad'))
    def explain_anxiety(self):
        self.declare(Fact(explanation="La ansiedad puede ser causada por preocupaciones excesivas o miedo a situaciones futuras. Es una respuesta natural del cuerpo al estrés, pero puede ser abrumadora si no se maneja adecuadamente."))

    @Rule(Symptom(type='depresion'))
    def explain_depression(self):
        self.declare(Fact(explanation="La depresión puede ser causada por una combinación de factores genéticos, biológicos, ambientales y psicológicos. Puede manifestarse como sentimientos persistentes de tristeza, falta de interés en actividades, cambios en el apetito y dificultad para concentrarse."))

    @Rule(Symptom(type='fatiga'))
    def explain_fatigue(self):
        self.declare(Fact(explanation="La fatiga puede ser causada por falta de sueño, estrés, mala alimentación o falta de actividad física. También puede ser un síntoma de condiciones médicas subyacentes, como anemia o hipotiroidismo."))
    
    @Rule(Symptom(type='insomnio'))
    def explain_insomnia(self):
        self.declare(Fact(explanation="El insomnio puede ser causado por una variedad de factores, incluidos el estrés, la ansiedad, los hábitos de sueño irregulares, el consumo de cafeína o ciertas condiciones médicas. La falta de sueño puede tener un impacto significativo en el estado de ánimo y el funcionamiento diario."))

    @Rule(Emotion(state='triste'))
    def explain_sadness(self):
        self.declare(Fact(explanation="La tristeza es una emoción natural que puede ser desencadenada por eventos estresantes, pérdidas personales o cambios en la vida. Es importante reconocer y expresar estas emociones para procesarlas de manera saludable."))

    @Rule(Context(situation='problemas_familiares'))
    def explain_family_problems(self):
            self.declare(Fact(explanation="Los problemas familiares pueden causar estrés, ansiedad y conflicto emocional. Es importante comunicarse abierta y honestamente con los miembros de la familia para resolver problemas y mantener relaciones saludables."))

    @Rule(Context(situation='dificultades_en_el_trabajo'))
    def explain_work_issues(self):
        self.declare(Fact(explanation="Las dificultades en el trabajo pueden ser una fuente significativa de estrés y ansiedad. Es importante buscar apoyo y desarrollar estrategias para manejar el estrés laboral de manera efectiva."))
   
    


    
    





