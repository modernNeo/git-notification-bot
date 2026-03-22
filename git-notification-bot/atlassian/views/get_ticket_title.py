import requests
from django.conf import settings


def token_is_valid(jira_tag: str | None) -> bool:
    response = __get_jira_issue_response(jira_tag)
    return response is not None and response.status_code == 200


def get_ticket_title(jira_tag: str | None) -> str | None:
    response = __get_jira_issue_response(jira_tag)
    if response is None or response.status_code != 200:
        return None
    return response.json()['fields']['summary']


def __get_jira_issue_response(jira_tag: str | None) -> requests.Response | None:
    if settings.ATLASSIAN_SUBNET is None or settings.JIRA_API_TOKEN is None or jira_tag is None:
        return None

    # Get the tenant UUID
    tenant_url = f"https://{settings.ATLASSIAN_SUBNET}.atlassian.net/_edge/tenant_info"
    tenant_uuid = requests.get(tenant_url).json()['cloudId']

    # Get the actual issue
    return requests.get(
        f"https://api.atlassian.com/ex/jira/{tenant_uuid}/rest/api/3/issue/{jira_tag}",
        headers={"authorization": f"Basic {settings.JIRA_API_TOKEN}"},
        params={"fields": "summary"}
    )
