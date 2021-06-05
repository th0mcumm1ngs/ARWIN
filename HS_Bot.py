from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
import json

with open('keysAndHttpAddresses.json', 'r') as data_file:
    keysAndHttpAddresses = json.load(data_file)

updater = Updater(token = keysAndHttpAddresses["telegram-token"])

dispatcher = updater.dispatcher

def start(update, context):
    with open('HS_Bot_HTML_files/start.html', 'r') as file:
        data = file.read()
    context.bot.send_message(chat_id=update.effective_chat.id, text = data, parse_mode = 'HTML')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()