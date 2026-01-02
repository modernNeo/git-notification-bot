import json

import requests
from django.conf import settings

from bitbucket_webhook.views.messages_to_send import MessagesToSend


def send_messages(messages_to_send: MessagesToSend):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {settings.SLACK_BOT_USER_OAUTH_TOKEN}"
    }
    for message_to_send in messages_to_send.messages_to_send:
        resp = requests.post("https://slack.com/api/chat.postMessage", headers=headers,
                      data=json.dumps({"channel": message_to_send['channel'], "blocks": message_to_send['blocks']}))
        print(resp.status_code)

