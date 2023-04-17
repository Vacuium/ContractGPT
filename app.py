import mysql
from flask import Flask, request, render_template,session,redirect,url_for,flash
from flask_mysqldb import MySQL
import mysql.connector
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

global chat_dict
chat_dict = {}

global config
config = configparser.ConfigParser()
config.read('config.ini')

class Config(object):
    SECRET_KEY = "DJFAJLAJAFKLJQ"

app = Flask(__name__)

@app.route('/')
def go():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="zhang2021238A",
            database="comp7300"
        )

        # Check if email and password match in the database
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            # If email and password are correct, set user session and redirect to index page
            # Add your session handling code here
            session['email'] = email
            return redirect(url_for("index"))
        else:
            # If email and password are incorrect, show error message
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)

@app.route('/register',methods=['get','post'])
def register():
    # Get form data from request object
    email = request.form.get('email')
    password = request.form.get('password')
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zhang2021238A",
        database="comp7300"
    )
    cursor = conn.cursor()

    # Insert form data into database
    cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()
    return render_template('register.html')

@app.route('/newChat', methods=['POST','GET'])
def newChat():
    global config
    global chat_dict
    code = request.get_json()['code'] # Get the code from the form submission

    prompt = 'You are the smart contract itself below. And you have to answer question about yourself i.e., the smart contract.\n'
    prompt += code if code else ''
    chatbot = Chatbot(api_key=config['CHATGPT']['API_KEY'])
    response = chatbot.ask(prompt = prompt)
    username = session.get('email')
    chat_dict[username]['chatbot'] = chatbot
    chat_dict[username]['og_response'] = response
    logging.info(f'{username}: {prompt}')
    logging.info(f'chat_dict: {chat_dict}')
    # return redirect(url_for("final"))
    # return render_template('streamChat.html')

# @app.route('/ogResponse', methods = ['Get'])
# def ogResponse():
#     global chat_dict
#     username = session.get('email')
#     response = chat_dict[username]['og_response']
#     return response

@app.route('/submit', methods = ['POST'])
def submit():
    global chat_dict
    username = session.get('email')
    chatbot = chat_dict[username]

    text = request.get_json()['text']
    answer = chatbot.ask(prompt = text)
    return answer

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/final')
def final():
    global chat_dict
    username = session.get('email')
    response = chat_dict[username]['og_response']
    return render_template('streamChat.html', og_response = response)

if __name__ == '__main__':
    # app.config["BASE_URL"] = public_url
    app.config.from_object(Config())
    app.run(debug=True) # Run the Flask app in debug mode