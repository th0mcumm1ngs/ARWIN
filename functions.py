import telegram, json

# Open all necessary JSON files.
with open('keysAndHttpAddresses.json', 'r') as data_file:
    keysAndHttpAddresses = json.load(data_file)

bot = telegram.Bot(token = keysAndHttpAddresses["telegram-token"])

def send_message(recepient_id, message):
    bot.sendMessage(chat_id = recepient_id, text = message)