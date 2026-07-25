import json

from slack.models import SlackInstallation
from slack.views.bot_workspace_admin_queries import attempt_slack_query_for_workspace_owners, get_custom_bot_admins


def parse_app_config_json(slack_team_obj: SlackInstallation):
    app_config = json.load(open('slack/views/app_config.json', 'r', encoding='utf-8'))

    workspace_owner_mentions = " ".join(
        [f"<@{admin_id}>" for admin_id in attempt_slack_query_for_workspace_owners(slack_team_obj)]
    )
    if len(workspace_owner_mentions) == 0:
        raise Exception("No workspace admins detected")

    for block in app_config.get('blocks', []):
        element = block.get('element', {})
        if element.get('action_id') == 'git_notification_bot_admin_input':
            label = block.get('label', {})
            label_text = label.get('text', 'Git Notification Bot Admins')
            label['text'] = f"{label_text}{workspace_owner_mentions}"
            block['label'] = label
            element['initial_users'] = list(get_custom_bot_admins(slack_team_obj))
            print(block)
        elif element.get('action_id') == 'atlassian_subnet_input':
            element['initial_value'] = slack_team_obj.atlassian_subnet

    return app_config
