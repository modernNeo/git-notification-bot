from slack.models import SlackInstallation
from slack.views.get_bot_admins import get_bot_admins


def include_custom_workspace_owners_for_initials_list(app_config_json, slack_team_obj: SlackInstallation):
    for block in app_config_json.get('blocks', []):
        element = block.get('element', {})
        if element.get('action_id') == 'git_notification_bot_admins':
            element['initial_users'] = list(get_bot_admins(slack_team_obj))
            print(element['initial_users'])

    return app_config_json
