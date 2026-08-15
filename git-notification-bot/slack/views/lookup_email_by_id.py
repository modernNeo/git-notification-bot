import requests


def lookup_email_by_id(bot_token, slack_user_id) -> str | None:
    resp = requests.get(
        "https://slack.com/api/users.info",
        headers={'Authorization': f"Bearer {bot_token}"},
        params={'user': slack_user_id}
    ).json()
    return resp['user']['profile']['email']
