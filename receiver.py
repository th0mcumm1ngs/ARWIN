# File is used to recieve incoming web requests.

import datetime
from flask import Flask
from flask import request

app = Flask(__name__)

# Simple ping. Used by othere HomeSystem Syetems to check the system is online.
@app.route("/")
def ping():
    return "Connection Succesful"

@app.route("/sendData", methods=['POST'])
def recieve_data():
    # Recieve the JSON data from the request.
    data = str(request.json)

    # Change all single quotes to double quotes (Due to Apple Shortcuts Error).
    for c in data:
        if c == "\'":
            new_data = data.replace("\'", '\"')
        else:
            pass

    # Get the current date and time.
    date = datetime.datetime.now()
    # Create file and set the date and time as the name.
    file = open(f"DataInterchange/{date}.json", 'w')
    # Write the JSON data to the file.
    file.write(new_data)
    file.close()
    # Return confirmation message to the user.
    return 'Data Recieved'

if __name__ == "__main__":
    app.run()