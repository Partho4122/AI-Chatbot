from flask import Flask, render_template, request, jsonify
from chatbot import ChatBot

app = Flask(__name__)
chatbot = ChatBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']
    response = chatbot.run_chatbot(message)  # Pass the user input to the method
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run()
