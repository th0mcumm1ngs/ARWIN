# File is used to recieve incoming web requests.

import datetime
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def ping():
    return "Connection Succesful"

@app.route("/sendData", methods=['POST'])
def recieve_data():
    data = str(request.json)

    for c in data:
        if c == "\'":
            new_data = data.replace("\'", '\"')
        else:
            pass
        
    date = datetime.datetime.now()
    file = open(f"RequestProcessing/{date}.json", 'w')
    file.write(new_data)
    file.close()
    return 'Data Recieved'

if __name__ == "__main__":
    app.run()