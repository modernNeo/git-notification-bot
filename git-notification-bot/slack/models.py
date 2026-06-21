from django.db import models


class SlackInstallation(models.Model):
    app_id = models.CharField(max_length=255, help_text="App ID")
    authed_user = models.CharField(max_length=255, help_text="Authorized User ID")
    bot_token = models.CharField(max_length=255, help_text="Permanent bot access token (starts with xoxb-)")
    bot_user_id = models.CharField(max_length=255, help_text="Bot User's ID")
    team_id = models.CharField(max_length=50, primary_key=True, help_text="Slack Workspace ID (starts with T)")
    team_name = models.CharField(max_length=255, blank=True, null=True)
    enterprise_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="Slack Enterprise Grid ID (starts with E)")
    installed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_name or self.team_id}"
