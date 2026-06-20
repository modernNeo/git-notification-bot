from django.db import models

from core.models import ClientConfig as core_config  # noqa: N813


# Create your models here.

class ClientConfig(models.Model):
    slack_bot_user_oauth_token = models.CharField(
        null=True,
        blank=True
    )
    client = models.ForeignKey(
        core_config, on_delete=models.CASCADE
    )


class SlackInstallation(models.Model):
    team_id = models.CharField(max_length=50, primary_key=True, help_text="Slack Workspace ID (starts with T)")
    bot_token = models.CharField(max_length=255, help_text="Permanent bot access token (starts with xoxb-)")
    team_name = models.CharField(max_length=255, blank=True, null=True)
    enterprise_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="Slack Enterprise Grid ID (starts with E)")
    installed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_name or self.team_id}"
