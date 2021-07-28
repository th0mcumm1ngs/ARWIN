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

## How To Install
This project was designed to be run on a Raspberry Pi. It may work on other systems but there is no guarantee.

There are 2 ways to go about this:

1. Install directly to your Raspberry Pi.

2. Download to an external computer and send the files over to the Raspberry Pi.

I prefer Option 2 as I've found Raspberry Pi's can be hard to work with.

### Option 1
1. Open Chromium on your Raspberry Pi and navigate to the [GitHub Repository](https://github.com/TomCummings07/HomeSystem).

2. Under the Releases menu on the right-hand side, click on the latest release. <sup>3</sup>

3. Scroll to the assets section and download either **Source Code.zip** or **Source Code.tar.gz**.

4. Unzip the file and move the HomeSystem folder to your Home Directory. <sup>4</sup>

5. Open 4 terminals all in the HomeSystem Directory. In terminal 1 type `python3 main.py`, in terminal 2 type `python3 HS_Bot.py`, in terminal 3 type `python3 receiver.py` and in terminal 4 type `./ngrok http 5000`.

### Option 2
1. On your external computer, open the [GitHub Repository](https://github.com/TomCummings07/HomeSystem) in your browser.

2. Under the Releases menu on the right-hand side, click on the latest release. <sup>3</sup>

3. Scroll to the assets section and download either **Source Code.zip** or **Source Code.tar.gz**.

4. Unzip the file and put it anywhere. Leave it in the downloads folder if it is there automatically.

5. Install [Croc](https://github.com/schollz/croc) on both your external computer and your Raspberry Pi:

    1. Open a new terminal.
    2. Type `curl https://getcroc.schollz.com | bash`

6. On your external computer, open a new terminal in the parent to the HomeSystem Directory and type:
    
        croc send HomeSystem
    
    You will be given a code phrase. Note it down.

7. On your Raspberry Pi, open a new terminal in your Home Directory<sup>4</sup> and type:

        croc [Your code phrase]

8. Still on your Raspberry Pi, open 4 terminals all in the HomeSystem Directory. In terminal 1 type `python3 main.py`, in terminal 2 type `python3 HS_Bot.py`, in terminal 3 type `python3 receiver.py` and in terminal 4 type `./ngrok http 5000`.

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

<sup>3</sup> Ensure to use the latest release and not just clone the repository. This is crucial since the repository may be unstable.

<sup>4</sup> Usually called Pi unless you have changed it.