import json, os, time, functions, datetime

run = True

while run:

    # Request Processing System
    # How it works:
    # The output of the Flask Server and Telegram Bot are stored in .json files in the path 'DataInterchange'.
    # The main.py file, this file, then filters through that directory and finds the .json files, retrieves the data in them and processes it accordingly.

	try:
		files = os.listdir('DataInterchange')
		
		for file in files:
			name, ext = os.path.splitext(file)
			if ext == ".json":
				with open(f'DataInterchange/{file}', 'r') as data_file:
					data = json.load(data_file)
				os.remove(f'DataInterchange/{file}')

				if data["reqType"] == "telegram":

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
								functions.send_message(recepient_id = data["chatID"], message = "Sorry, there seems to have been an error. If you need help with a command call '/help [COMMAND NAME]'.\n\nNote: Dont include the '/' of the command that you need assistance with in your command.")

							else:
								senderName = functions.get_user_from_chatID(data["chatID"])

								text = f"Announcement from {senderName}. \"{given_message}\""

								for i in recipients:
									if i == "everyone":
										recipient = HS_Data["alert_channel_id"]

									else:
										recipient = HS_Data["users"][i]["chatID"]

									functions.send_message(recepient_id = recipient, message = text)

								functions.send_message(recepient_id = data["chatID"], message = "Your message was sent successfully.")


						announce()

				elif data["reqType"] == "flask":
					pass

			
			else:
				os.remove(f'DataInterchange/{file}')
	
	except:
		pass