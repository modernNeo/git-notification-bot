import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.LogRequestData import log_request_data


@method_decorator(csrf_exempt, name='dispatch')
class SlackInteractivityView(View):

    def post(self, request, *args, **kwargs):
        log_request_data(request)

        if request.POST.get("ssl_check") == "1":
            return HttpResponse(status=200)

        raw_payload = request.POST.get("payload")
        if not raw_payload:
            return HttpResponse("Missing payload", status=400)

        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        payload_type = payload.get("type")

        # Route to specific internal class handlers based on interaction type [1]
        if payload_type == "block_actions":
            return self._handle_block_actions(payload)

        elif payload_type == "view_submission":
            return self._handle_view_submission(payload)

        return HttpResponse(status=200)

    def _handle_block_actions(self, payload):
        """Fires when the owner clicks the configuration button in App Home"""
        # Slack wraps actions in a list [1]
        actions = payload.get("actions", [])
        if not actions:
            return HttpResponse(status=200)

        action_id = actions[0].get("action_id")

        if action_id == "open_config_button":
            trigger_id = payload["trigger_id"]

            # Modal configuration scheme using Block Kit
            modal_view = {
                "type": "modal",
                "title": {  # Modals require a title block
                    "type": "plain_text",
                    "text": "Settings"
                },
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

            self._call_slack_api("https://slack.com", {"trigger_id": trigger_id, "view": modal_view})

        return HttpResponse(status=200)

    def _handle_view_submission(self, payload):
        """Fires when the user clicks 'Save' on the interactive modal"""
        view = payload.get("view", {})

        if view.get("callback_id") == "workspace_config_modal":
            state_values = view["state"]["values"]

            # Extract values precisely matching your block_id and action_id strings [1]
            field_value = state_values["config_field_one"]["input_value_one"]["value"]
            workspace_id = payload["team"]["id"]

            # Persistent save logic inside your backend
            success = self._save_to_database(workspace_id, field_value)

            if not success:
                # If database layer fails, send an in-modal validation error message [1]
                return JsonResponse({
                    "response_action": "errors",
                    "errors": {
                        "config_field_one": "Database connection error. Try again."
                    }
                })

            # Clear response payload closes the modal window automatically [1]
            return HttpResponse(status=200)

        return HttpResponse(status=200)

    def _call_slack_api(self, url, json_data):
        """Network helper to post back to Slack API network routers [1]"""
        headers = {
            "Authorization": f"Bearer {self.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json; charset=utf-8"
        }
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()

    def _save_to_database(self, workspace_id, configuration_value):
        """Placeholder for updating your custom Django Model fields"""
        try:
            # Example Django ORM command:
            # BotSettings.objects.update_or_create(
            #     workspace_id=workspace_id,
            #     defaults={'setting_value': configuration_value}
            # )
            return True
        except Exception:
            return False
