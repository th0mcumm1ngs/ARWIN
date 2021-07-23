import telegram, json

# Open all necessary JSON files.
with open('data.json', 'r') as data_file:
    HS_Data = json.load(data_file)

bot = telegram.Bot(token = HS_Data["API_TOKENS"]["telegram-token"])

def send_message(recepient_id, message):
    bot.sendMessage(chat_id = recepient_id, text = message, parse_mode = "HTML")

def get_user_from_chatID(chatID):
    chatIDs = HS_Data["chatID_to_name"]

    # Checks if the Chat ID provided by the initiator is in the known Chat IDs

    if chatID in chatIDs:
        return HS_Data["chatID_to_name"][chatID]

    else:
        return "Guest"