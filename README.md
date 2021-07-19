# HomeSystem

This repo includes the code for the RPi Server that holds all of the HomeSystem data.

## How It Works
In a nutshell, the system works by sending requests as JSON data across the **DataInterchange** folder.

### Example Scenario 1 - Telegram Bot for user interaction
A user sends a command to the Telegram Bot. The bot then recognises the command, initiates the **send_request()** function and passes the parameters **command** and **chatID**. This function then adds one to the **reqID_counter** system-wide variable — This is used to ensure that every request ID is unique. Then, a dictionary is created with the request ID, command type and chatID from earlier. After that, the dictionary is turned into JSON<sup>1</sup> and packaged into a .json file. This is then sent to the **DataInterchange** folder. The **main.py** file constantly looks through the **DataInterchange** and parses the JSON data in the files. It then acts upon the command specified in the request and sends the output to the chatID obtained earlier.

### Example Scenario 2 - Flask Request Receiver for computer generated requests
The reciever.py file contains a Flask Server. This can recieve JSON data from other systems and devices - i.e. a Smart Screen, Smart Camera, Siri Shortcuts, etc. It then packages this JSON data and sends it to the DataInterchange in the same way as in Scenario 1.

This has multiple applications including:
- Using the Server as a private cloud to store data from other devices.
- Handling requests from non-users<sup>2</sup>

## Footnotes
<sup>1</sup> An exapmle of this:

    data = {
        "reqID":reqID,
        "command":command,
        "chatID":chatID
    }

<sup>2</sup> Examples of this could be:
- A Motion Sensor has detected motion and wants to alert the system.
- A smart screen wishes to retrieve information from the **FileSystem**.