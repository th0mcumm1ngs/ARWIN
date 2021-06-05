# File is used to recieve incoming web requests.

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def ping():
    return "Connection Succesful"

if __name__ == "__main__":
    app.run()