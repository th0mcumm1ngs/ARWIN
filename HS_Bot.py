from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
import json, datetime

with open('keysAndHttpAddresses.json', 'r') as data_file:
    keysAndHttpAddresses = json.load(data_file)

updater = Updater(token = keysAndHttpAddresses["telegram-token"])

def send_request(command, chatID):
    # Get and update reqID_counter variable.
    with open('globalVariables.json', 'r') as data_file:
        globalVariables = json.load(data_file)

    # Update the variable by adding 1

    reqID = globalVariables["reqID_counter"] + 1

    globalVariables["reqID_counter"] = reqID

    with open('globalVariables.json', 'w') as data_file:
        json.dump(globalVariables, data_file, indent = 4)

    data = {
        "reqType":"telegram",
        "reqID":reqID,
        "command":command,
        "chatID":chatID
    }

    # Get the current date and time.
    date = datetime.datetime.now()
    # Create file and set the date and time as the name.
    with open(f"DataInterchange/{date}.json", 'w') as file:
        # Write the JSON data to the file.
        json.dump(data, file, indent = 4)

dispatcher = updater.dispatcher

def start(update, context):
    with open('HS_Bot_HTML_files/start.html', 'r') as file:
        data = file.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text = data, parse_mode = 'HTML')

def time(update, context):
    send_request(command = "time", chatID = update.effective_chat.id)

time_handler = CommandHandler('time', time)
dispatcher.add_handler(time_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()