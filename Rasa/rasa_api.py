import requests

def send_to_rasa(message):

    url = "http://localhost:5005/webhooks/rest/webhook"

    payload = {
        "sender": "user",
        "message": message
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()[0]["text"]

    except:
        return "Rasa server is not running."