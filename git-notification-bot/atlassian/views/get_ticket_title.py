import requests

from slack.models import SlackInstallation


def token_is_valid(slack_team_obj: SlackInstallation) -> bool:
    response = __get_jira_issue_response("BOT-123", slack_team_obj)
    return response is not None and response.status_code == 200


def get_ticket_title(jira_tag: str, slack_team_obj: SlackInstallation) -> str | None:
    response = __get_jira_issue_response(jira_tag, slack_team_obj)
    if response is None or response.status_code != 200:
        return None
    return response.json()['fields']['summary']


def __get_jira_issue_response(jira_tag: str, slack_team_obj: SlackInstallation) -> requests.Response | None:
    if slack_team_obj.atlassian_subnet is None or slack_team_obj.jira_api_token is None:
        return None

    # Get the tenant UUID
    tenant_url = f"https://{slack_team_obj.atlassian_subnet}.atlassian.net/_edge/tenant_info"
    tenant_uuid = requests.get(tenant_url).json()['cloudId']

    # Get the actual issue
    return requests.get(
        f"https://api.atlassian.com/ex/jira/{tenant_uuid}/rest/api/3/issue/{jira_tag}",
        headers={"authorization": f"Basic {slack_team_obj.jira_api_token}"},
        params={"fields": "summary"}
    )
