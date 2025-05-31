import requests

def send_slack_alert(message, webhook_url):
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("✅ Slack alert sent!")
    else:
        print(f"❌ Failed to send alert. Status: {response.status_code}")
