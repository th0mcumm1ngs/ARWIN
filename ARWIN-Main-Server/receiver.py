from flask import Flask, request
from waitress import serve
import json

serverSettings = json.load(open('settings.json', 'r'))

serverAddress = serverSettings["SERVER_ADDRESSES"]["main_server"]

app = Flask(__name__)

@app.route("/GET", methods = ["GET"])
def GET():
    pass

@app.route("/POST", methods = ["POST"])
def POST():
    pass

if __name__ == "__main__":
    serve(app = app, host = serverAddress, port = 8080)