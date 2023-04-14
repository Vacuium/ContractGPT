from flask import Flask, request, render_template
from revChatGPT.V3 import Chatbot

import configparser
import logging


def ask_contract(contract):
    config = configparser.ConfigParser()
    config.read('config.ini')
    chatbot = Chatbot(api_key=config['CHATGPT']['API_KEY'])

    prompt = 'Pretend that you are the smart contract itself below. And you have to answer question about yourself i.e., the smart contract.\n'
    answer = chatbot.ask(prompt = prompt + contract)
    return answer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') # Render the HTML template

@app.route('/submit', methods=['POST'])
def submit():
    code = request.get_json()['code'] # Get the code from the form submission
    answer = ask_contract(code) # Print the code in the terminal
    return answer # Return the code back to the frontend to display below the input section

if __name__ == '__main__':
    app.run(host = '10.0.0.4', port = 5000, debug=True) # Run the Flask app in debug mode