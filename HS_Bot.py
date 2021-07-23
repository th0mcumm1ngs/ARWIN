from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
import json, datetime

with open('data.json', 'r') as data_file:
    HS_Data = json.load(data_file)

updater = Updater(token = HS_Data["API_TOKENS"]["telegram-token"])

def send_request(command, chatID, args):
    # Get and update reqID_counter variable.
    with open('data.json', 'r') as data_file:
        HS_Data = json.load(data_file)

    # Update the variable by adding 1

    reqID = HS_Data["globalVariables"]["reqID_counter"] + 1

    HS_Data["globalVariables"]["reqID_counter"] = reqID

    with open('data.json', 'w') as data_file:
        json.dump(HS_Data, data_file, indent = 4)

    data = {
        "reqType":"telegram",
        "reqID":reqID,
        "command":command,
        "chatID":str(chatID),
        "args": args
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

def announce(update, context):
    send_request(command = "announce", chatID = update.effective_chat.id, args = context.args)

briefing_handler = CommandHandler('announce', announce)
dispatcher.add_handler(briefing_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()