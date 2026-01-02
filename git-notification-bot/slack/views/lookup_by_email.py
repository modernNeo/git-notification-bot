import requests
from django.conf import settings


def lookup_user_id_by_email(email:str|None) -> str|None:
    if email is None:
        return None
    resp = requests.get(
        f"https://slack.com/api/users.lookupByEmail?email={email}",
        headers={'Authorization' : f"Bearer {settings.SLACK_BOT_USER_OAUTH_TOKEN}"}
    ).json()
    return resp['user']['id']