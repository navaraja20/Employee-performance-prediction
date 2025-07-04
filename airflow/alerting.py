import requests

def send_teams_alert(webhook_url, message):
    headers = {"Content-Type": "application/json"}
    data = {"text": message}
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Request to Teams returned error {response.status_code}, {response.text}")
