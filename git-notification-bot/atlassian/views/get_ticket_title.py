import requests
from django.conf import settings


def get_ticket_title(jira_tag:str|None) -> None|str:
    if settings.ATLASSIAN_SUBNET is None or settings.JIRA_API_TOKEN is None or jira_tag is None:
        return None
    response = requests.get(f"https://{settings.ATLASSIAN_SUBNET}.atlassian.net/_edge/tenant_info")
    tenant_uuid = response.json()['cloudId']
    response = requests.get(
        f"https://api.atlassian.com/ex/jira/{tenant_uuid}/rest/api/3/issue/{jira_tag}",
        headers={"authorization": f"Basic {settings.JIRA_API_TOKEN}"},
        params={"fields": "summary"}
    )
    return response.json()['fields']['summary']
