from flask import Flask, render_template, request
from waitress import serve
import datetime, json

serverSettings = json.load(open('settings.json', 'r'))

serverAddress = serverSettings["SERVER_ADDRESSES"]["web_server"]

app = Flask(__name__)

# Website Routes

@app.route("/")
def home():
    return render_template('home.html')

# Server Processes

@app.route("/ping")
def ping():
    return "Connection Succesful"

if __name__ == "__main__":
    serve(app = app, host = serverAddress, port = 8080)