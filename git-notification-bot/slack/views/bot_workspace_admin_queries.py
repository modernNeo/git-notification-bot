import requests
from django.db import models

from slack.models import SlackInstallation, BotWorkspaceAdmin


def attempt_slack_query_for_workspace_owners(slack_team_obj: SlackInstallation):
    workspace_admins = []
    cursor = None

    while True:
        params = {"cursor": cursor} if cursor else {}
        resp = _get_users_list(slack_team_obj.bot_token, params)
        body = resp.json()
        # print("get_owners Response Body (JSON):", json.dumps(body, indent=4))

        if body.get("ok"):
            # Extract owners from the current page
            for member in body.get("members", []):
                if (member.get("is_owner") or member.get("is_primary_owner")) \
                        and not member.get("deleted") \
                        and not member.get("is_bot"):
                    workspace_admins.append({
                        "user_id": member["id"],
                        "primary_owner": member["is_primary_owner"],
                        "owner": member["is_owner"],
                    })
            # Check if there is another page
            cursor = body.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
        else:
            error = body.get("error")
            if error == "ratelimited":
                return query_db_for_workspace_owners(slack_team_obj)
            else:
                raise Exception(f"got unexpected error of {error}")

    owners = [
        BotWorkspaceAdmin(
            user_id=workspace_admin["user_id"], workspace=slack_team_obj,
            primary_workspace_owner=workspace_admin["primary_owner"],
            workspace_owner=workspace_admin["owner"])
        for workspace_admin in workspace_admins
    ]
    BotWorkspaceAdmin.objects.bulk_create(owners, ignore_conflicts=True)

    return query_db_for_workspace_owners(slack_team_obj)


def _get_users_list(bot_token, params):
    return requests.get(
        "https://slack.com/api/users.list",
        headers={'Authorization': f"Bearer {bot_token}"},
        params=params
    )


def query_db_for_workspace_owners(slack_team_obj: SlackInstallation):
    return list(
        slack_team_obj.admins.filter(
            models.Q(primary_workspace_owner=True) | models.Q(workspace_owner=True)
        ).values_list('user_id', flat=True)
    )


def get_all_bot_admins(slack_team_obj: SlackInstallation):
    return list(slack_team_obj.admins.values_list('user_id', flat=True))


def get_custom_bot_admins(slack_team_obj: SlackInstallation):
    return list(
        slack_team_obj.admins.filter(
            models.Q(primary_workspace_owner=False) & models.Q(workspace_owner=False)
        ).values_list('user_id', flat=True)
    )
