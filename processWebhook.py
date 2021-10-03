import os

import flask
from flask import send_from_directory, request

from dotenv import load_dotenv
load_dotenv()

from menu import showMenu

app = flask.Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

# from waSendMessage import sendMessage

userChats = {}

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    global userChats
    try:
        # print(request.get_data())
        message = request.form['Body']
        senderId = request.form['From'].split('+')[1]
        
        print(f'Message --> {message}')
        print(f'Sender id --> {senderId}')

        showMenu(senderId, message)
        
        # res = sendMessage(senderId=senderId, message=message)
        # print(f'This is the response --> {res}')

        print("done processing request")
        return '200'
    except Exception as e:
        print(e)
        return '401'

@app.route('/callback', methods=['POST'])
def callback():
    print(request.get_data)
    return '200'

if __name__ == "__main__":
    app.run(port=5000, debug=True)