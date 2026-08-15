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

    atlassian_subnet = models.CharField(max_length=255, blank=True, null=True)
    atlassian_cloud_id = models.CharField(max_length=255, blank=True, null=True)
    jira_api_token = models.CharField(max_length=255, blank=True, null=True)

    # jira_tag_extraction_source = models.CharField(max_length=255, blank=True, null=True)
    # # branch name
    # # PR Title
    # # PR description
    #
    # jira_tag_pattern_matcher = models.CharField(max_length=255, blank=True, null=True)
    # bitbucket_secret = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.team_name or self.team_id}"


class BotWorkspaceAdmin(models.Model):
    user_id = models.CharField(max_length=255, help_text="Bot Admin's User ID")
    workspace = models.ForeignKey(
        SlackInstallation,
        on_delete=models.CASCADE,
        related_name="admins",
        help_text="The Slack workspace this admin belongs to"
    )
    primary_workspace_owner = models.BooleanField(
        default=False,
        help_text=(
            "They hold the absolute highest level of permissions. "
            "In addition to having all the same administrative capabilities as a regular Workspace Owner, "
            "only the Primary Owner can delete the workspace or transfer primary ownership to another member. "
            "There can only be one Workspace Primary Owner per workspace."
        )
    )
    workspace_owner = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'workspace'], name='unique_bot_workspace_admin'),
            # This ensures only ONE row per workspace can have primary_workspace_owner = True
            models.UniqueConstraint(
                fields=['workspace'],
                condition=models.Q(primary_workspace_owner=True),
                name='unique_primary_workspace_owner_per_workspace'
            )
        ]

    def __str__(self):
        return f"Bot Admin {self.user_id} for {self.workspace}"
