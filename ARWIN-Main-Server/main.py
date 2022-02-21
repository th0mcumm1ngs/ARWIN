import functions
from datetime import *
import json
import requests

# Initialise variables.
lastPerformedRecurringActions = None

# Initialise the main loop.

run = True

while run:

    with open('ARWIN-Main-Server/data.json', 'r') as data_file:
        dataFile = json.load(data_file)

    # Try Except statement used to ensure that the loop doesnt break.
    try:
        # Recurring Actions
        ## Get the current date and time.
        now = datetime.now()
        ## Get the current date and time in a string format.
        now_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # Checks if the recurring actions have been completed in the last minute.
        if now.strftime("%H:%M") != lastPerformedRecurringActions:

            lastPerformedRecurringActions = now.strftime("%H:%M")

            # System Checks
            if "00:00:00" in now_string:
                functions.logLastPerformedRecurringAction(now_string, "systemChecks")
                # Perform server maintenance. (Update checks, security scans, etc.)
                for server in dataFile["SERVERS"]:
                    if server != "main-server":
                        serverAddress = dataFile["SERVERS"][server]["IP-address"]
                    else:
                        pass

        # Request Processing System
        # This is a recurring action that is used to check if there are any new files in the DataInterchange directory.

    except Exception as err:
        # Check if the error is a common error with no effect.
        if str(err) in ["Expecting value: line 1 column 1 (char 0)"]:
            pass
        else:
            # If there is an exception, send the details to the developer.
            functions.alertDev(content = err)

# This code should never run as there is a try-except statement. In the event that it does the system can be restarted.
functions.alertDev(content = "Loop in main.py has been broken causing the program to quit. Maintenance needed immediately.")