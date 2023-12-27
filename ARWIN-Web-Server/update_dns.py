import requests, json

host = "@"
domain_name = "thomcummings.dev"
ddns_password = json.load(open("data.json"))["API_KEYS+SECRETS"]["DDNS_PASSWORD"]

requestResponse = requests.get(f"https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain_name}&password={ddns_password}")