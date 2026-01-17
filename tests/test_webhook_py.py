import requests

print("Sending 'Hi' to webhook...")
try:
    resp = requests.post(
        "http://localhost:8000/webhook",
        data={"From": "whatsapp:+918446041580", "Body": "Hi"}
    )
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
