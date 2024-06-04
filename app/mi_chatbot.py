from experta import Fact, Rule, KnowledgeEngine
from bayesian_model import predict_emotion_and_symptom

class Message(Fact):
    pass

class Explanation(Fact):
    pass

class Chatbot(KnowledgeEngine):
    @Rule(Message(content="Hello"))
    def greet(self):
        self.declare(Fact(response="Hello! How can I help you?"))

    @Rule(Message(content="Goodbye"))
    def farewell(self):
        self.declare(Fact(response="See you later!"))

class Symptom(Fact):
    pass

class Emotion(Fact):
    pass

class Context(Fact):
    pass

class MentalHealthChatbot(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.inference = predict_emotion_and_symptom  # Bayesian inference function
    
    def infer_response(self, emotion, symptom, context):
        # Convert emotional and contextual variables to a format the inference function can use
        emotion_mapping = {0: 'happy', 1: 'sad', 2: 'stressed'}
        symptom_mapping = {0: 'no symptoms', 1: 'fatigue', 2: 'insomnia', 3: 'anxiety'}
        context_mapping = {0: 'work_difficulties', 1: 'family_problems'}

        emotion_state = emotion_mapping[emotion]
        context_situation = context_mapping[context]
        emotion, symptom, context = self.inference(emotion_state, context_situation)

        if emotion == "happy":
            return f"The most likely emotion is {emotion} and the most likely symptom is {symptom} in the context without context"
        else:
            return f"The most likely emotion is {emotion} and the most likely symptom is {symptom} in the context {context}"

    @Rule(Symptom(type='anxiety') & Emotion(state='stressed'))
    def handle_anxiety_and_stress(self):
        self.declare(Fact(response=self.infer_response(2, 3, 0)))

    @Rule(Symptom(type='depression') & Context(situation='family_problems'))
    def handle_depression_and_family_problems(self):
        self.declare(Fact(response=self.infer_response(1, 1, 0)))

    @Rule(Emotion(state='sad') & ~Symptom(type='depression'))
    def handle_sadness_without_depression(self):
        self.declare(Fact(response=self.infer_response(1, 0, 0)))

    @Rule(Emotion(state='stressed') & Context(situation='work_difficulties'))
    def handle_stress_and_work_issues(self):
        self.declare(Fact(response=self.infer_response(2, 0, 1)))

    @Rule(Symptom(type='fatigue') & Emotion(state='sad') & ~Symptom(type='insomnia'))
    def handle_fatigue_and_sadness_without_insomnia(self):
        self.declare(Fact(response=self.infer_response(1, 1, 0)))

    @Rule(Symptom(type='insomnia') & Symptom(type='anxiety'))
    def handle_insomnia_and_anxiety(self):
        self.declare(Fact(response=self.infer_response(2, 3, 0)))

    @Rule(Symptom(type='fatigue') & Symptom(type='insomnia'))
    def handle_fatigue_and_insomnia(self):
        self.declare(Fact(response=self.infer_response(2, 2, 0)))

    @Rule(Symptom(type='depression') & Emotion(state='sad') & Context(situation='work_difficulties'))
    def handle_depression_sadness_work_issues(self):
        self.declare(Fact(response=self.infer_response(1, 1, 1)))

    @Rule(Symptom(type='anxiety'))
    def handle_anxiety(self):
        self.declare(Fact(response=self.infer_response(2, 3, 0)))

    @Rule(Symptom(type='depression'))
    def handle_depression(self):
        self.declare(Fact(response=self.infer_response(1, 1, 0)))

    @Rule(Emotion(state='sad'))
    def handle_sadness(self):
        self.declare(Fact(response=self.infer_response(1, 0, 0)))

    @Rule(Emotion(state='stressed'))
    def handle_stress(self):
        self.declare(Fact(response=self.infer_response(2, 0, 0)))

    @Rule(Context(situation='family_problems'))
    def handle_family_problems(self):
        self.declare(Fact(response=self.infer_response(0, 0, 0)))

    @Rule(Emotion(state='happy'))
    def handle_happiness(self):
        self.declare(Fact(response=self.infer_response(0, 0, 0)))

    @Rule(Symptom(type='insomnia'))
    def handle_insomnia(self):
        self.declare(Fact(response=self.infer_response(2, 2, 0)))

    @Rule(Symptom(type='fatigue'))
    def handle_fatigue(self):
        self.declare(Fact(response=self.infer_response(1, 1, 0)))

    @Rule(Context(situation='work_difficulties'))
    def handle_work_issues(self):
        self.declare(Fact(response=self.infer_response(2, 0, 1)))

    @Rule(Message(content="Hello"))
    def greet(self):
        self.declare(Fact(response="Hello! How can I help you?"))

    @Rule(Message(content="Goodbye"))
    def farewell(self):
        self.declare(Fact(response="See you later!"))

    @Rule(Symptom(type='anxiety'))
    def explain_anxiety(self):
        self.declare(Fact(explanation="Anxiety can be caused by excessive worries or fear of future situations. It is a natural body response to stress, but it can be overwhelming if not managed properly."))

    @Rule(Symptom(type='depression'))
    def explain_depression(self):
        self.declare(Fact(explanation="Depression can be caused by a combination of genetic, biological, environmental, and psychological factors. It can manifest as persistent feelings of sadness, lack of interest in activities, changes in appetite, and difficulty concentrating."))

    @Rule(Symptom(type='fatigue'))
    def explain_fatigue(self):
        self.declare(Fact(explanation="Fatigue can be caused by lack of sleep, stress, poor diet, or lack of physical activity. It can also be a symptom of underlying medical conditions, such as anemia or hypothyroidism."))

    @Rule(Symptom(type='insomnia'))
    def explain_insomnia(self):
        self.declare(Fact(explanation="Insomnia can be caused by a variety of factors, including stress, anxiety, irregular sleep habits, caffeine consumption, or certain medical conditions. Lack of sleep can significantly impact mood and daily functioning."))

    @Rule(Emotion(state='sad'))
    def explain_sadness(self):
        self.declare(Fact(explanation="Sadness is a natural emotion that can be triggered by stressful events, personal losses, or life changes. It is important to recognize and express these emotions to process them healthily."))

    @Rule(Context(situation='family_problems'))
    def explain_family_problems(self):
        self.declare(Fact(explanation="Family problems can cause stress, anxiety, and emotional conflict. It is important to communicate openly and honestly with family members to resolve issues and maintain healthy relationships."))

    @Rule(Context(situation='work_difficulties'))
    def explain_work_issues(self):
        self.declare(Fact(explanation="Work difficulties can be a significant source of stress and anxiety. It is important to seek support and develop strategies to manage work-related stress effectively."))

   
    


    
    





