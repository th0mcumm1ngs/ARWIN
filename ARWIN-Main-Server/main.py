import functions
import json, os

# Load the settings file.
serverSettings = json.load(open('settings.json', 'r'))

while True:

    dataFile = json.load(open('data.json', 'r'))

    # Try Except statement used to ensure that the loop doesnt break.
    try:
        # Request Processing System
        # This is a recurring action that is used to check if there are any new files in the DataInterchange directory.

        for file in os.listdir('DataInterchange'):
            name, ext = os.path.splitext(file)
            if ext == ".json":
                dataFile = json.load(open(f'DataInterchange/{file}', 'r'))

                # The different processes go here.
                
                os.rename(f'DataInterchange/{file}', f'bin/processed_requests/{file}')

            elif name == ".blank":
                pass
            else:
                os.rename(f'DataInterchange/{file}', f'bin/misplaced_files/{file}')

    except Exception as err:
        # Check if the error is a common error with no effect.
        if str(err) in ["Expecting value: line 1 column 1 (char 0)"]:
            pass
        else:
            # If there is an exception, send the details to the developer.
            functions.alertDev(content = err)

# This code should never run as there is a try-except statement. In the event that it does the system can be restarted.
functions.alertDev(content = "Loop in main.py has been broken causing the program to quit. Maintenance needed immediately.")