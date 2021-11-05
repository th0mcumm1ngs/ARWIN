import json, os, functions, dateutil.relativedelta
from datetime import *

run = True

while run:

	try:
		with open('data.json', 'r') as data_file:
			HS_Data = json.load(data_file)

		# Recurring Actions.

	except Exception as err:
		# Check if the error is a common error with no effect.
		if str(err) == "Expecting value: line 1 column 1 (char 0)":
			pass
		else:
			# If there is an exception, send the details to the developer.
			functions.flagError(description = err)

    # Request Processing System
    # How it works:
    # The output of the Flask Server and Telegram Bot are stored in JSON files in the path 'DataInterchange'.
    # The main.py file, this file, then filters through that directory and finds the JSON files, moves them to the cache, retrieves the data in them and processes it accordingly.

	# Try Except statement used to ensure that the loop doesnt break.
	try:
		files = os.listdir('DataInterchange')
		
		for file in files:
			# Get the name and extention of the file
			name, ext = os.path.splitext(file)
			# Checks if the file is JSON data. Essentially checks whether a file was put there by accident or not.
			if ext == ".json":
				with open(f'DataInterchange/{file}', 'r') as data_file:
					data = json.load(data_file)
				os.rename(f'DataInterchange/{file}', f'FileSystem/bin/requests/{file}')

				# Checks if the request came from telegram.
				if data["reqType"] == "telegram":
					pass

				# Checks if the request came from flask.
				elif data["reqType"] == "flask":
					pass
			
			elif name == ".blank":
				pass
			# If the file wasn't JSON, it is deleted.
			else:
				os.remove(f'DataInterchange/{file}')
	
	except Exception as err:
		# Check if the error is a common error with no effect.
		if str(err) == "Expecting value: line 1 column 1 (char 0)":
			pass
		else:
			# If there is an exception, send the details to the developer.
			functions.flagError(description = err)

# This error should never run as there is a try, except statement. In the event that it does the system can be restarted.
functions.flagError(description = "Loop in main.py has been broken causing program to quit. Maintenance needed immediately.")