import json, os, time, functions, datetime, sys

run = True

while run:

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
				os.rename(f'DataInterchange/{file}', f'FileSystem/Cache/requests/{file}')

				# Checks if the request came from telegram.
				if data["reqType"] == "telegram":

					# Handles the /announce command.
					if data["command"] == "announce":
						# Function used to keep variables isolated.
						def announce():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							# Set variable defaults
							recipients = []
							at_least_one_recipient = False
							given_message = ""
							word = 0
							error = False

							for i in data["args"]:
								if i.lower() in HS_Data["users"]:
									at_least_one_recipient = True
									recipients.append(i.lower())

								elif i.lower() == "everyone":
									at_least_one_recipient = True
									recipients.append(i.lower())

								else:
									if word >= 1:
										given_message += " " + i

									else:
										given_message += i
									
									word += 1

							if at_least_one_recipient == False:
								error = True

							if error == True:
								# If the user has typed the command incorrectly, they are informed and instructed on the correct syntax.
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need help with a command call '/help [COMMAND NAME]'.\n\nNote: Dont include the '/' of the command that you need assistance with in your command.")

							else:
								senderName = functions.get_user_from_chatID(data["chatID"])

								text = f"Announcement from {senderName}. \"{given_message}\""

								# Loop used to send the announcement to each recipient.
								for i in recipients:
									if i == "everyone":
										recipient = HS_Data["alert_channel_id"]

									else:
										recipient = HS_Data["users"][i]["chatID"]

									functions.send_message(recepient_id = recipient, message = text)

								functions.send_message(recepient_id = data["chatID"], message = "Your message was sent successfully.")

						announce()
					
					if data["command"] == "newstopwatch":
						def new_stopwatch():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							# Used to stitch the words passed as arguments together.
							words = 0
							name = ""

							for i in data["args"]:
								if words >= 1:
									name += " " + i

								else:
									name += i
								
								words += 1

							# Checks if a stopwatch with the same name already exists.
							if name not in HS_Data["stopwatchesAndTimers"]:
								HS_Data["stopwatchesAndTimers"][name] = str(datetime.datetime.now())

								with open('data.json', 'w') as data_file:
									json.dump(HS_Data, data_file, indent = 4)

								functions.send_message(recepient_id = data["chatID"], message = f"Stopwatch successfully created. Type \"/checkstopwatch {name}\" to get the time since it was created.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, a stopwatch with that name already exists.")

						new_stopwatch()

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