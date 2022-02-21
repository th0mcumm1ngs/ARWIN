from flask import Flask, request
from waitress import serve
import json

with open('ARWIN-Main-Server/data.json', 'r') as data_file:
    dataFile = json.load(data_file)

serverAddress = dataFile["SERVERS"]["main-server"]["IP-address"]

app = Flask(__name__)

@app.route("/POST", methods = ["POST"])
def POST():
    pass

if __name__ == "__main__":
    serve(app = app, host=serverAddress, port=8080)