import json, os, time, functions, sys, dateutil.relativedelta
from datetime import *

run = True

while run:

	try:
		with open('data.json', 'r') as data_file:
			HS_Data = json.load(data_file)

		# Recurring Actions.

		## Poweroff Command.
		if HS_Data["poweroff"]["status"] == True:
			time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

			formattedRequestTime = datetime.strptime(HS_Data["poweroff"]["requestTime"], '%Y-%m-%d %H:%M:%S')

			# Check if it has been 60 seconds since the request was made.
			if str(time_now) == str(formattedRequestTime + timedelta(seconds = 60)):

				functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "The system has now temporarily deactivated. All requests will be suspended until it is reactivated. You will be notified of this event.")

				HS_Data["poweroff"]["status"] = False
				HS_Data["poweroff"]["requestTime"] = ""

				with open('data.json', 'w') as data_file:
					json.dump(HS_Data, data_file, indent = 4)

				os.system('shutdown now -h')

		## Restart Command
		if HS_Data["restart"]["status"] == True:
			time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

			formattedRequestTime = datetime.strptime(HS_Data["restart"]["requestTime"], '%Y-%m-%d %H:%M:%S')

			# Check if it has been 60 seconds since the request was made.
			if str(time_now) == str(formattedRequestTime + timedelta(seconds = 60)):

				functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "The system has now restarted. You will be notified when the restart has completed.")

				HS_Data["restart"]["status"] = False
				HS_Data["restart"]["requestTime"] = ""

				with open('data.json', 'w') as data_file:
					json.dump(HS_Data, data_file, indent = 4)

				os.system('shutdown now -r')

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
				os.rename(f'DataInterchange/{file}', f'FileSystem/Cache/requests/{file}')

				# Checks if the request came from telegram.
				if data["reqType"] == "telegram":

					# Handles the /help command.
					if data["command"] == "help":
						def help():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							if len(data["args"]) == 1:
								commands = [
									'announce',
									'newstopwatch',
									'checkstopwatch',
									'resetstopwatch',
									'deletestopwatch',
									'poweroff'
								]

								command_name = data["args"][0]

								if command_name in commands:
									with open(f'HS_Bot_HTML_files/help/{command_name}.html') as file:
										text = file.read()

									functions.send_message(recepient_id = data["chatID"], message = text)

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, that command doesn't exist.")

							elif len(data["args"]) == 0:
								with open('HS_Bot_HTML_files/help/help.html') as file:
									text = file.read()
									
								functions.send_message(recepient_id = data["chatID"], message = text)

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. Please ensure there is only one argument.")

						help()

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
							recipients_done = False
							everyone_passed = False

							for i in data["args"]:
								if recipients_done == False:
									if i.lower() in HS_Data["users"]:
										at_least_one_recipient = True
										recipients.append(i.lower())

									elif i.lower() == "everyone":
										everyone_passed = True
										at_least_one_recipient = True
										recipients.append(i.lower())

									else:
										recipients_done = True
										if word >= 1:
											given_message += " " + i

										else:
											given_message += i
										
										word += 1
								
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
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

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
					
					# Handles the stopwatch commands.
					
					## Handles the /newstopwatch command.
					if data["command"] == "newstopwatch":
						def new_stopwatch():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							if len(data["args"]) != 0:
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
									HS_Data["stopwatchesAndTimers"][name] = str(datetime.now())

									with open('data.json', 'w') as data_file:
										json.dump(HS_Data, data_file, indent = 4)

									functions.send_message(recepient_id = data["chatID"], message = f"Stopwatch successfully created. Type \"/checkstopwatch {name}\" to obtain the time since it was started.")

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, a stopwatch with that name already exists.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

						new_stopwatch()
					
					## Handles the /checkstopwatch command.
					if data["command"] == "checkstopwatch":
						def check_stopwatch():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							if len(data["args"]) != 0:
								# Used to stitch the words passed as arguments together.
								words = 0
								name = ""

								for i in data["args"]:
									if words >= 1:
										name += " " + i

									else:
										name += i
									
									words += 1

								# Checks if the stopwatch exists.
								if name in HS_Data["stopwatchesAndTimers"]:
									time_started = datetime.strptime(str(HS_Data["stopwatchesAndTimers"][name]), "%Y-%m-%d %H:%M:%S.%f")

									time_now = datetime.now()

									time_elapsed = dateutil.relativedelta.relativedelta(time_now, time_started)

									seconds = time_elapsed.seconds
									
									minutes = time_elapsed.minutes

									hours = time_elapsed.hours
									
									days = time_elapsed.days

									weeks = time_elapsed.weeks

									years = time_elapsed.years

									# Make sure all variables are whole numbers.
									seconds = int(seconds)

									minutes = int(minutes)

									hours = int(hours)

									days = int(days)

									weeks = int(weeks)

									years = int(years)

									timeframes_used = 0
									tf1 = None
									tf2 = None
									tf3 = None
									tf4 = None
									tf5 = None
									tf6 = None

									if years != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = years
										elif tf2 == None:
											tf2 = years
										elif tf3 == None:
											tf3 = years
										elif tf4 == None:
											tf4 = years
										elif tf5 == None:
											tf5 = years
										elif tf6 == None:
											tf6 = years
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")
											
									if weeks != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = weeks
										elif tf2 == None:
											tf2 = weeks
										elif tf3 == None:
											tf3 = weeks
										elif tf4 == None:
											tf4 = seconds
										elif tf5 == None:
											tf5 = weeks
										elif tf6 == None:
											tf6 = weeks
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")

									if days != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = days
										elif tf2 == None:
											tf2 = days
										elif tf3 == None:
											tf3 = days
										elif tf4 == None:
											tf4 = days
										elif tf5 == None:
											tf5 = days
										elif tf6 == None:
											tf6 = days
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")

									if hours != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = hours
										elif tf2 == None:
											tf2 = hours
										elif tf3 == None:
											tf3 = hours
										elif tf4 == None:
											tf4 = hours
										elif tf5 == None:
											tf5 = hours
										elif tf6 == None:
											tf6 = hours
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")

									if minutes != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = minutes
										elif tf2 == None:
											tf2 = minutes
										elif tf3 == None:
											tf3 = minutes
										elif tf4 == None:
											tf4 = minutes
										elif tf5 == None:
											tf5 = minutes
										elif tf6 == None:
											tf6 = minutes
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")

									if seconds != 0:
										timeframes_used += 1
										if tf1 == None:
											tf1 = seconds
										elif tf2 == None:
											tf2 = seconds
										elif tf3 == None:
											tf3 = seconds
										elif tf4 == None:
											tf4 = seconds
										elif tf5 == None:
											tf5 = seconds
										elif tf6 == None:
											tf6 = seconds
										else:
											functions.flagError(description = "The /checkstopwatch command failed: No 'tf' slots remaining.")

									if timeframes_used == 0:
										functions.flagError(description = "The /checkstopwatch command failed: The timeframes_used variable ended at 0.")

									text_templates = {
										"1": f"It has been {tf1} seconds since the stopwatch was started",
										"2": f"It has been {tf1} minutes and {tf2} seconds since the stopwatch was started",
										"3": f"It has been {tf1} hours, {tf2} minutes and {tf3} seconds since the stopwatch was started",
										"4": f"It has been {tf1} days, {tf2} hours, {tf3} minutes and {tf4} seconds since the stopwatch was started",
										"5": f"It has been {tf1} weeks, {tf2} days, {tf3} hours, {tf4} minutes and {tf5} seconds since the stopwatch was started",
										"6": f"It has been {tf1} years, {tf2} weeks, {tf3} days, {tf4} hours, {tf5} minutes and {tf6} seconds since the stopwatch was started"
									}

									if timeframes_used == 1:
										text = text_templates["1"]

									if timeframes_used == 2:
										text = text_templates["2"]

									if timeframes_used == 3:
										text = text_templates["3"]

									if timeframes_used == 4:
										text = text_templates["4"]

									if timeframes_used == 5:
										text = text_templates["5"]

									if timeframes_used == 6:
										text = text_templates["6"]

									functions.send_message(recepient_id = data["chatID"], message = text)

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, a stopwatch with that name doesn't exist.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

						check_stopwatch()

					## Handles the /resetstopwatch command.
					if data["command"] == "resetstopwatch":
						def reset_stopwatch():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							if len(data["args"]) != 0:
								# Used to stitch the words passed as arguments together.
								words = 0
								name = ""

								for i in data["args"]:
									if words >= 1:
										name += " " + i

									else:
										name += i
									
									words += 1

								if name in HS_Data["stopwatchesAndTimers"]:
									HS_Data["stopwatchesAndTimers"][name] = str(datetime.now())

									with open('data.json', 'w') as data_file:
										json.dump(HS_Data, data_file, indent = 4)

									functions.send_message(recepient_id = data["chatID"], message = f"Stopwatch successfully reset. Type \"/checkstopwatch {name}\" to get the time since it was started.")

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, a stopwatch with that name doesn't exist.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

						reset_stopwatch()

					## Handles the /deletestopwatch command.
					if data["command"] == "deletestopwatch":
						def delete_stopwatch():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							if len(data["args"]) != 0:
								# Used to stitch the words passed as arguments together.
								words = 0
								name = ""

								for i in data["args"]:
									if words >= 1:
										name += " " + i

									else:
										name += i
									
									words += 1

								# Checks if the stopwatch exists.
								if name in HS_Data["stopwatchesAndTimers"]:
									del HS_Data["stopwatchesAndTimers"][name]

									with open('data.json', 'w') as data_file:
										json.dump(HS_Data, data_file, indent = 4)

									functions.send_message(recepient_id = data["chatID"], message = f"Stopwatch successfully deleted.")

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, a stopwatch with that name doesn't exist.")
							
							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

						delete_stopwatch()

					## Handles the /poweroff command.
					if data["command"] == "poweroff":
						def power_off_system():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							# This is for activating the power off sequence.
							if len(data["args"]) == 1:
								if data["args"][0] == HS_Data["TOKENS_AND_KEYS"]["adminPassword"]:

									functions.send_message(recepient_id = data["chatID"], message = "The system will turn off in 1 minute. Use the /poweroff false [adminPassword] to cancel this.")
									functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "Hello. The system will be temporarily deactivating in 1 minute.")

									HS_Data["poweroff"]["status"] = True
									HS_Data["poweroff"]["requestTime"] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

									with open('data.json', 'w') as data_file:
										json.dump(HS_Data, data_file, indent = 4)

								else:
									functions.send_message(recepient_id = data["chatID"], message = "The admin password is incorrect.")
							
							# This is for aborting the deactivation sequence.
							elif len(data["args"]) == 2:
								if data["args"][0] == "false":

									if data["args"][1] == HS_Data["TOKENS_AND_KEYS"]["adminPassword"]:

										if HS_Data["poweroff"]["status"] == True:

											HS_Data["poweroff"]["status"] = False
											HS_Data["poweroff"]["requestTime"] = ""

											with open('data.json', 'w') as data_file:
												json.dump(HS_Data, data_file, indent = 4)

											functions.send_message(recepient_id = data["chatID"], message = "System deactivation has been aborted.")
											functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "System deactivation has been aborted. It will no longer be temporarily deactivated and will continue to function normally.")

										else:
											functions.send_message(recepient_id = data["chatID"], message = "System is not scheduled for deactivation.")

									else:
										functions.send_message(recepient_id = data["chatID"], message = "The admin password provided is incorrect.")

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")
						
						power_off_system()

					## Handles the /restart command.
					if data["command"] == "restart":
						def restart_system():
							with open('data.json', 'r') as data_file:
								HS_Data = json.load(data_file)

							# This is for activating the restart sequence.
							if len(data["args"]) == 1:
								if data["args"][0] == HS_Data["TOKENS_AND_KEYS"]["adminPassword"]:

									functions.send_message(recepient_id = data["chatID"], message = "The system will restart in 1 minute. Use the /restart false [adminPassword] to cancel this.")
									functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "Hello. The system will be restarting in 1 minute.")

									HS_Data["restart"]["status"] = True
									HS_Data["restart"]["requestTime"] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

									with open('data.json', 'w') as data_file:
										json.dump(HS_Data, data_file, indent = 4)

								else:
									functions.send_message(recepient_id = data["chatID"], message = "The admin password is incorrect.")
							
							# This is for aborting the restart sequence.
							elif len(data["args"]) == 2:
								if data["args"][0] == "false":

									if data["args"][1] == HS_Data["TOKENS_AND_KEYS"]["adminPassword"]:

										if HS_Data["restart"]["status"] == True:

											HS_Data["restart"]["status"] = False
											HS_Data["restart"]["requestTime"] = ""

											with open('data.json', 'w') as data_file:
												json.dump(HS_Data, data_file, indent = 4)

											functions.send_message(recepient_id = data["chatID"], message = "System restart has been aborted.")
											functions.send_message(recepient_id = HS_Data["alert_channel_id"], message = "System restart has been aborted. It will no longer be restarted and will continue to function normally.")

										else:
											functions.send_message(recepient_id = data["chatID"], message = "System is not scheduled for restart.")

									else:
										functions.send_message(recepient_id = data["chatID"], message = "The admin password provided is incorrect.")

								else:
									functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")

							else:
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need assistance with a command call '/help [COMMAND NAME]'.\n\nNote: Don’t include the '/' of the command that you need assistance with in your command.")
						
						restart_system()

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