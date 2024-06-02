import requests

url = "https://api.brightdata.com/zone/whitelist"

payload = {
    #"zone": "<string>",
    "ip": "192.168.100.28"
}
headers = {
    "Authorization": "Bearer e12bce7b-7f6a-475b-960a-2385db5c6a2b",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)