import json, requests, datetime
from cryptography.fernet import Fernet

# Open data file.
with open('data.json', 'r') as data_file:
    HS_Data = json.load(data_file)

def send_message(recepient_id, message):
    pass

def make_request(endpoint_url, reqData):
    requests.post(url = endpoint_url, json = reqData)

def flagError(description):
    pass

# Encryption + Decryption

def encrypt(data):
    encryptionManager = Fernet(HS_Data["ENCRYPTION_KEY"])

    # If data type is bytes, just encrypt.
    if type(data) == bytes:
        encryptedMessage = encryptionManager.encrypt(data)

    # If it's not, encode then encrypt.
    else:
        encryptedMessage = encryptionManager.encrypt(data.encode())

    return encryptedMessage

def decrypt(data: bytes):
    if type(data) == bytes:
        encryptionManager = Fernet(HS_Data["ENCRYPTION_KEY"])

        decodedMessage = encryptionManager.decrypt(data)

        return decodedMessage
        
    else:
        raise TypeError("Data type must be bytes.")