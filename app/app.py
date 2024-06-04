from flask import Flask, request, render_template, jsonify
from experta import Fact

app = Flask(__name__)

# Import the chatbot logic
from mi_chatbot import Chatbot, Message, MentalHealthChatbot, Symptom, Emotion, Context, Explanation
from bayesian_model import predict_emotion_and_symptom

# Create an instance of the chatbot
chatbot = Chatbot()
chatbot_engine = MentalHealthChatbot()
chatbot_engine.reset()

# Global variable to store the information of the last detected emotion
last_emotion = None

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global last_emotion
    
    if request.method == 'POST':
        data = request.json
        user_input = data.get('message')
        
        # Reset the engine to clear any previous facts
        chatbot_engine.reset()

        # Declare facts based on user input
        if 'hello' in user_input.lower():
            chatbot_engine.declare(Message(content='Hello'))
        elif 'goodbye' in user_input.lower():
            chatbot_engine.declare(Message(content='Goodbye'))        
        else:
            # Identify the user's emotion
            emotions = []

            if 'sad' in user_input.lower():
                emotions.append('sad')
            if 'stressed' in user_input.lower():
                emotions.append('stressed')
            if 'happy' in user_input.lower():
                emotions.append('happy')
            
            for emotion in emotions:
                chatbot_engine.declare(Emotion(state=emotion))
                last_emotion = emotion
        
        chatbot_engine.run()
        
        # Get the response from the expert system
        response_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Fact and 'response' in fact), None)
        explanation_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Explanation), None)

        response = response_fact['response'] if response_fact else None
        explanation = explanation_fact['info'] if explanation_fact else None

        if not response:
            response = "Would you like to know more about this emotion?"
        
        return jsonify({'response': response, 'explanation': explanation})
    
    return render_template('basic.html')

@app.route('/expand', methods=['POST'])
def expand():
    global last_emotion
    
    if request.method == 'POST':
        data = request.json
        user_input = data.get('message')

        if last_emotion:
            if 'yes' in user_input.lower():
                chatbot_engine.reset()
                chatbot_engine.declare(Emotion(state=last_emotion))
                chatbot_engine.declare(Message(content='Expand'))
                chatbot_engine.run()

                explanation_fact = next((fact for fact in chatbot_engine.facts.values() if fact.__class__ == Explanation), None)
                explanation = explanation_fact['info'] if explanation_fact else None

                last_emotion = None  # Reset last_emotion to None after handling the expansion request

                return jsonify({'response': explanation})

            elif 'no' in user_input.lower():
                last_emotion = None  # Reset last_emotion to None if the user does not want to expand the information
                return jsonify({'response': "Understood, how else can I help you?"})

        return jsonify({'response': "Sorry, I didn't understand your response."})

if __name__ == '__main__':
    app.run(debug=True)





