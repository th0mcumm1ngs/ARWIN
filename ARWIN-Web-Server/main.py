# File is used to recieve incoming web requests.

import datetime, json
from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

# Website Routes

@app.route("/")
def home():
    return render_template('home.html')

# Background Processes

@app.route("/ping")
def ping():
    return "Connection Succesful"

if __name__ == "__main__":
    serve(app = app, host='127.0.0.1', port=8080)