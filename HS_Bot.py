from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
import json, datetime

with open('data.json', 'r') as data_file:
    HS_Data = json.load(data_file)

updater = Updater(token = HS_Data["TOKENS_AND_KEYS"]["telegram-token"])

def send_request(command, chatID, args):
    # Get and update reqID_counter variable.
    with open('data.json', 'r') as data_file:
        HS_Data = json.load(data_file)

    # Update the variable by adding 1
    reqID = HS_Data["globalVariables"]["reqID_counter"] + 1

    HS_Data["globalVariables"]["reqID_counter"] = reqID

    with open('data.json', 'w') as data_file:
        json.dump(HS_Data, data_file, indent = 4)

    # Compile the data.
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

def help(update, context):
    send_request(command = "help", chatID = update.effective_chat.id, args = context.args)

def announce(update, context):
    send_request(command = "announce", chatID = update.effective_chat.id, args = context.args)

def new_stopwatch(update, context):
    send_request(command = "newstopwatch", chatID = update.effective_chat.id, args = context.args)

def check_stopwatch(update, context):
    send_request(command = "checkstopwatch", chatID = update.effective_chat.id, args = context.args)

def reset_stopwatch(update, context):
    send_request(command = "resetstopwatch", chatID = update.effective_chat.id, args = context.args)

def delete_stopwatch(update, context):
    send_request(command = "deletestopwatch", chatID = update.effective_chat.id, args = context.args)

# Admin Commands

def power_off_system(update, context):
    send_request(command = "poweroff", chatID = update.effective_chat.id, args = context.args)

def restart_system(update, context):
    send_request(command = "restart", chatID = update.effective_chat.id, args = context.args)

# Add the command handlers
briefing_handler = CommandHandler('announce', announce)
dispatcher.add_handler(briefing_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

new_stopwatch_handler = CommandHandler('newstopwatch', new_stopwatch)
dispatcher.add_handler(new_stopwatch_handler)

check_stopwatch_handler = CommandHandler('checkstopwatch', check_stopwatch)
dispatcher.add_handler(check_stopwatch_handler)

reset_stopwatch_handler = CommandHandler('resetstopwatch', reset_stopwatch)
dispatcher.add_handler(reset_stopwatch_handler)

delete_stopwatch_handler = CommandHandler('deletestopwatch', delete_stopwatch)
dispatcher.add_handler(delete_stopwatch_handler)

# Admin Commands

power_off_system_handler = CommandHandler('poweroff', power_off_system)
dispatcher.add_handler(power_off_system_handler)

restart_system_handler = CommandHandler('restart', restart_system)
dispatcher.add_handler(restart_system_handler)

updater.start_polling()