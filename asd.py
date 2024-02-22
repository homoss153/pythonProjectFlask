import requests
import json

BASE = "http://127.0.0.1:5000/"

payload = {"user_id": 120,
        "type_transfer": 1,
        "name": "test",
        "description": "test",
        "price": 1212,
        "date_time": "test",
        "icon": "test",
        "category": "test",
        "payment_name": "test"}

test = {
    "user_id": 120
}

headers = {'accept': 'application/json'}
response = requests.post("http://127.0.0.1:5000/get_transfer", json=test)

print(response.text)