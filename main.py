import json, os, time

run = True

while run:

    # Request Processing System
    # How it works:
    # The output of the Flask Server and Telegram Bot are stored in .json files in the path 'DataInterchange'.
    # The main.py file, this file, then filters through that directory and finds the .json files, retrieves the data in them and processes it accordingly.

	files = os.listdir('DataInterchange')
    
	for file in files:
		name, ext = os.path.splitext(file)
		if ext == ".json":
			data_file = open(f'DataInterchange/{file}', 'r')
			data = data_file.read()
			data_file.close()
			os.remove(f'DataInterchange/{file}')
		
		else:
			os.remove(f'DataInterchange/{file}')