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

					if data["command"] == "time":
						functions.send_message(recepient_id = data["chatID"], message = f"The current time is: {str(datetime.datetime.now())}")

				elif data["reqType"] == "flask":
					pass

			
			else:
				os.remove(f'DataInterchange/{file}')
	
	except:
		pass