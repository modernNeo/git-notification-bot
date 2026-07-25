from slack.models import SlackInstallation
from slack.views.get_owners import get_owners


def include_workspace_owners(app_config_json, slack_team_obj: SlackInstallation):
    admins = get_owners(slack_team_obj.bot_token)
    admin_mentions = " ".join([f"<@{admin_id}>" for admin_id in admins])

    for block in app_config_json.get('blocks', []):
        element = block.get('element', {})
        if element.get('action_id') == 'git_notification_bot_admins':
            # Convert the input block into a read-only section block
            label = block.get('label', {})
            label['text'] = f"{label.get('text', 'Git Notification Bot Admins')}{admin_mentions}"
            block['label'] = label
            break

    return app_config_json
