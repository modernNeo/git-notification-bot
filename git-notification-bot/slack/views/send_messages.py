import json

import requests

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.models import SlackInstallation


def send_messages(messages_to_send: MessagesToSend, slack_team_obj: SlackInstallation):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {slack_team_obj.bot_token}"
    }
    for message_to_send in messages_to_send.messages_to_send:
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            data=json.dumps({"channel": message_to_send['channel'], "blocks": message_to_send['blocks']})
        )
        print(resp.status_code)


def send_ephemeral_messages(messages_to_send: MessagesToSend, slack_team_obj: SlackInstallation):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {slack_team_obj.bot_token}"
    }
    for message_to_send in messages_to_send.messages_to_send:
        resp = requests.post(
            "https://slack.com/api/chat.postEphemeral",
            headers=headers,
            data=json.dumps({"channel": message_to_send['channel'], "blocks": message_to_send['blocks']})
        )
        print(resp.status_code)
