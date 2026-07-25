from slack.models import SlackInstallation


def get_bot_admins(slack_team_obj: SlackInstallation):
    return slack_team_obj.admins.values_list('user_id', flat=True)
