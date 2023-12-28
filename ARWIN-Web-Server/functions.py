import requests, json

serverSettings = json.load(open('data.json', 'r'))

API_KEY = serverSettings["API_KEYS+SECRETS"]["TELEGRAM"]["TELEGRAM_API_KEY"]

def alert_dev(content):
    data = {
        'chat_id': serverSettings["API_KEYS+SECRETS"]["TELEGRAM"]["TELEGRAM_CHAT_ID"],
        'text': content
    }

    requests.post(f"https://api.telegram.org/bot{API_KEY}/sendMessage", json=data)