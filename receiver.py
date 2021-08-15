# File is used to recieve incoming web requests.

import datetime, json
from flask import Flask
from flask import request

app = Flask(__name__)

with open('data.json', 'r') as data_file:
    HS_Data = json.load(data_file)

# Simple ping. Used by othere HomeSystem Syetems to check the system is online.
@app.route("/")
def ping():
    return "Connection Succesful"

@app.route("/sendData", methods=['POST'])
def recieve_data():
    # Recieve the JSON data from the request.
    req_data = request.get_json()

    # Get and update reqID_counter variable.
    # Update the variable by adding 1

    reqID = HS_Data["globalVariables"]["reqID_counter"] + 1

    HS_Data["globalVariables"]["reqID_counter"] = reqID

    with open('data.json', 'w') as data_file:
        json.dump(HS_Data, data_file, indent = 4)

    # Compile the data.
    data = {
        "reqType":"flask",
        "reqID":reqID,
        "reqData":req_data
    }

    # Get the current date and time.
    date = datetime.datetime.now()
    # Create file and set the date and time as the name.
    with open(f"DataInterchange/{date}.json", 'w') as file:
        # Write the JSON data to the file.
        json.dump(data, file, indent = 4)
    # Return confirmation message to the user.
    return 'Data Recieved'

if __name__ == "__main__":
    app.run()