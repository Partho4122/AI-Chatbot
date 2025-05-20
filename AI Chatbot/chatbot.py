from flask import Flask, render_template, request, jsonify
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit

openai.api_key = "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"

model_engine = "text-davinci-002"
engine = pyttsx3.init()

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        pass

    def listen_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            input_text = r.recognize_google(audio)
            print("You: " + input_text)
            return input_text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Sorry, I'm having trouble accessing the speech recognition service.")
            return None

    def process_input(self, input_text):
        if not input_text:
            input_text = self.listen_input()
        if not input_text:
            return None

        if input_text.lower() in ["quit", "exit"]:
            return "quit"

        if 'time' in input_text.lower():
            answer = datetime.datetime.now().strftime('The time is %I:%M %p.')
        elif 'play' in input_text.lower():
            song = input_text.lower().replace('play', '')
            pywhatkit.playonyt(song)
            answer = f'Playing {song}'
        else:
            try:
                prompt = f"Q: {input_text}\nA: "
                response = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                answer = response.choices[0].text.strip()
            except openai.error.OpenAIError as e:
                answer = "Sorry, I'm having trouble accessing the OpenAI API."

        return answer

    def run_chatbot(self, input_text):
        # Process and respond to the input
        answer = self.process_input(input_text)
        return answer

# Create an instance of the chatbot
chatbot = ChatBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']
    answer = chatbot.run_chatbot(message)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
