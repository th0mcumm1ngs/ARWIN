import json, requests, telegram
from cryptography.fernet import Fernet

# Open data file.
with open('ARWIN-Main-Server/data.json', 'r') as data_file:
    dataFile = json.load(data_file)

def send_message(recepient_id, message):
    pass

def make_request(endpoint_url, reqData):
    requests.post(url = endpoint_url, json = reqData)

def alertDev(content):
    token = '5375317355:AAHXHsu2XvUZkzzs3GUsGM5Ge-bRCUnv-aI'
    bot = telegram.Bot(token = token)
    bot.sendMessage(chat_id = '1436572458', text = content)

def logLastPerformedRecurringAction(time, action):
    dataFile["RECURRING_ACTIONS"][action]["lastPerformed"] = time
    
    with open('ARWIN-Main-Server/data.json', 'w') as data_file:
        json.dump(dataFile, data_file, indent = 4)

# Encryption + Decryption

def encrypt(data):
    encryptionManager = Fernet(dataFile["ENCRYPTION_KEY"])

    # If data type is bytes, just encrypt.
    if type(data) == bytes:
        encryptedMessage = encryptionManager.encrypt(data)

    # If it's not, encode then encrypt.
    else:
        encryptedMessage = encryptionManager.encrypt(data.encode())

    return encryptedMessage

def decrypt(data: bytes):
    if type(data) == bytes:
        encryptionManager = Fernet(dataFile["ENCRYPTION_KEY"])

        decodedMessage = encryptionManager.decrypt(data)

        return decodedMessage
        
    else:
        raise TypeError("Data type must be bytes.")