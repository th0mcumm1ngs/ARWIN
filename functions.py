import telegram, json, requests, datetime

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

def make_request(endpoint_url, reqData):
    requests.post(url = endpoint_url, json = reqData)

def flagError(description):
    timeNow = datetime.datetime.now()

    dateAndTime = timeNow.strftime(f"%d/%m/%y at %H:%M:%S")

    text = f"Hello Tom. There was an error flagged on the {dateAndTime}.\n\n{description}"

    send_message(recepient_id = HS_Data["users"]["tom"]["chatID"], message = text)

    send_message(recepient_id = HS_Data["alert_channel_id"], message = "Hello. There seems to be a system error. The developers have been notified and this complication should be fixed shortly.\n\nThe system may be powered off during this time. You will most likely be notified, however, don’t be alarmed if commands are not replied to. They will be replied to as soon as the system is back online.\n\nThank you for your understanding.")