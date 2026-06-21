import json

import requests
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.LogRequestData import log_request_data
from slack.models import SlackInstallation


@method_decorator(csrf_exempt, name="dispatch")  # 3. Apply the exemption
class SlackEventSubscriptions(View):
    """Generates the secure state and redirects the user to Slack."""

    def get(self, request):
        log_request_data(request)
        return HttpResponse("GET SlackEventSubscriptions.")

    def post(self, request, *args, **kwargs):
        log_request_data(request)

        # 1. Safely parse the raw JSON body from Slack
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        # 2. STRUCTURAL FIX: Handle the URL Verification handshake
        if body.get("type") == "url_verification":
            return JsonResponse({"challenge": body.get("challenge")})

        # 3. Handle actual Slack events
        team_id = body.get("team_id")
        slack_team_obj = SlackInstallation.objects.filter(team_id=team_id).first()
        if slack_team_obj:
            event = body.get("event", {})
            # When a user clicks into your App Home tab
            if event.get("type") == "app_home_opened":
                user_id = event.get("user")
                self._publish_app_home(user_id, slack_team_obj.bot_token)

        # Always return a 200 OK to acknowledge receipt of the event
        return HttpResponse(status=200)

    def _publish_app_home(self, user_id, slack_token):
        """Pushes the initial Home Tab view containing your configuration button"""
        home_view = {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Bot Configurations",
                        "emoji": True
                    },
                    "level": 1
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "atlassian_subnet_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "atlassian_subnet_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Atlassian Subnet",
                        "emoji": True
                    },
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "jira_token_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "jira_token_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Jira API Token",
                        "emoji": True
                    },
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "jira_source_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "jira_source_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Jira Tag Extraction Source",
                        "emoji": True
                    },
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "jira_pattern_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "jira_pattern_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Jira Tag Pattern Matcher",
                        "emoji": True
                    },
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "bitbucket_secret_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "bitbucket_secret_input"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Bitbucket Secret",
                        "emoji": True
                    },
                    "optional": True
                },
                {
                    "type": "actions",
                    "block_id": "config_footer_buttons",
                    "elements": [
                        {
                            "type": "button",
                            "action_id": "app_home_submit_settings",
                            "text": {
                                "type": "plain_text",
                                "text": "Save Changes"
                            },
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "action_id": "app_home_cancel_settings",
                            "text": {
                                "type": "plain_text",
                                "text": "Reset Form"
                            },
                            "style": "danger"
                        }
                    ]
                }
            ]
        }

        resp = requests.post(
            "https://slack.com/api/views.publish",
            headers={
                "Authorization": f"Bearer {slack_token}",  # noqa F821
                "Content-Type": "application/json; charset=utf-8"
            },
            json={
                "user_id": user_id,
                "view": home_view
            }
        ).json()
        print(resp)

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackEventSubscriptions.")

    def put(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PUT SlackEventSubscriptions.")
