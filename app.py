from flask import Flask, request, render_template
from revChatGPT.V3 import Chatbot

import configparser
import logging
import os
import sys
# from pyngrok import ngrok

# port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000

# # Open a ngrok tunnel to the dev server
# public_url = ngrok.connect(port).public_url
# print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))



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
    # app.config["BASE_URL"] = public_url
    app.run(debug=True) # Run the Flask app in debug mode