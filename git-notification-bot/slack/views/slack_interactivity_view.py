import base64
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.log_request_data import log_request_data
from slack.models import SlackInstallation, BotWorkspaceAdmin
from slack.views.bot_workspace_admin_queries import attempt_slack_query_for_workspace_owners, get_custom_bot_admins
from slack.views.lookup_email_by_id import lookup_email_by_id
from slack.views.slack_event_subscriptions import SlackEventSubscriptions


def _parse_bot_admins(payload, slack_team_obj: SlackInstallation):
    current_admins_user_ids = list(get_custom_bot_admins(slack_team_obj))
    workspace_owner_ids = attempt_slack_query_for_workspace_owners(slack_team_obj)

    # filtering out the workspace owners since they are already bot admins
    selected_workspace_owner_ids = [
        selected_workspace_owner_id
        for selected_workspace_owner_id in _get_selected_workspace_owner_ids(payload)
        if selected_workspace_owner_id not in workspace_owner_ids
    ]

    ids_for_workspace_owners_to_delete = [
        current_admin_user_id
        for current_admin_user_id in current_admins_user_ids
        if current_admin_user_id not in selected_workspace_owner_ids
    ]

    ids_for_workspace_owners_to_create = [
        user_id for user_id in selected_workspace_owner_ids
        if user_id not in current_admins_user_ids
    ]

    workspace_owners_to_create = [
        BotWorkspaceAdmin(user_id=id_for_workspace_owners_to_create, workspace=slack_team_obj)
        for id_for_workspace_owners_to_create in ids_for_workspace_owners_to_create
    ]

    if len(workspace_owners_to_create) > 0:
        message = " ".join([f"saved {admin}\n" for admin in workspace_owners_to_create])
        print(f"{message}")
        BotWorkspaceAdmin.objects.bulk_create(workspace_owners_to_create, ignore_conflicts=True)
    deleted_admins = BotWorkspaceAdmin.objects.filter(user_id__in=ids_for_workspace_owners_to_delete)
    if len(deleted_admins) > 0:
        message = " ".join([f"deleted {admin}\n" for admin in deleted_admins])
        print(f"{message}")
        deleted_admins.delete()


def _get_selected_workspace_owner_ids(payload):
    view = payload.get("view", {})
    state = view.get("state", {})
    values = state.get("values", {})
    git_notification_bot_admins_block = values.get("git_notification_bot_admins_block", {})
    git_notification_bot_admin_input = git_notification_bot_admins_block.get(
        "git_notification_bot_admin_input", {})
    return git_notification_bot_admin_input.get("selected_users", [])


def _parse_atlassian_subnet(payload, slack_team_obj: SlackInstallation):
    selected_atlassian_subnet, selected_atlassian_cloud_id = _get_selected_atlassian_subnet(
        payload, slack_team_obj
    )
    if slack_team_obj.atlassian_subnet != selected_atlassian_subnet:
        slack_team_obj.atlassian_subnet = selected_atlassian_subnet
        slack_team_obj.atlassian_cloud_id = selected_atlassian_cloud_id


def _get_selected_atlassian_subnet(payload, slack_team_obj: SlackInstallation):
    view = payload.get("view", {})
    state = view.get("state", {})
    values = state.get("values", {})
    atlassian_subnet_block = values.get("atlassian_subnet_block", {})
    atlassian_subnet_input = atlassian_subnet_block.get("atlassian_subnet_input", {})
    selected_atlassian_subnet = atlassian_subnet_input.get("value", "")
    if selected_atlassian_subnet is None:
        selected_atlassian_subnet = ""
    selected_atlassian_cloud_id = None
    if len(selected_atlassian_subnet) > 0:
        tenant_url = f"https://{selected_atlassian_subnet}.atlassian.net/_edge/tenant_info"
        response = requests.get(tenant_url)
        if response.status_code == 200:
            selected_atlassian_cloud_id = response.json()['cloudId']
        else:
            # invalid subnet so just revert to what was previously set
            return slack_team_obj.atlassian_subnet, slack_team_obj.atlassian_cloud_id
    return selected_atlassian_subnet, selected_atlassian_cloud_id


def _parse_jira_token(payload, slack_team_obj: SlackInstallation):
    if slack_team_obj.atlassian_cloud_id is None:
        slack_team_obj.jira_api_token = None
        return
    view = payload.get("view", {})
    state = view.get("state", {})
    values = state.get("values", {})
    jira_token_block = values.get("jira_token_block", {})
    jira_token_input = jira_token_block.get("jira_token_input", {})
    selected_jira_token = jira_token_input.get("value", "")
    if selected_jira_token is None:
        slack_team_obj.jira_api_token = None
        return

    user = payload.get("user", {})
    user_id = user.get("id", None)
    url = f"https://api.atlassian.com/ex/jira/{slack_team_obj.atlassian_cloud_id}/rest/api/3/myself"
    email = lookup_email_by_id(slack_team_obj.bot_token, user_id)
    if email:
        creds = f"{email}:{selected_jira_token}"
        encoded_creds = base64.b64encode(creds.encode("utf-8")).decode("utf-8")
        response = requests.get(url, headers={"Authorization": f"Basic {encoded_creds}"})
        if response.status_code == 200:
            slack_team_obj.jira_api_token = selected_jira_token


@method_decorator(csrf_exempt, name='dispatch')
class SlackInteractivityView(View):

    def post(self, request, *args, **kwargs):
        log_request_data(request)

        raw_payload = request.POST.get("payload")
        if not raw_payload:
            return HttpResponse("Missing payload", status=400)

        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        if request.POST.get("ssl_check") == "1":
            return HttpResponse(status=200)

        team_id = payload.get("team").get("id")
        slack_team_obj = SlackInstallation.objects.filter(team_id=team_id).first()
        if slack_team_obj is None:
            return HttpResponse(f"Invalid Team ID {team_id}", status=400)

        payload_type = payload.get("type")

        # Route to specific internal class handlers based on interaction type [1]
        if payload_type == "block_actions":
            return self._handle_block_actions(payload, slack_team_obj)

        elif payload_type == "view_submission":
            return self._handle_view_submission(payload)

        return HttpResponse(status=200)

    def _handle_block_actions(self, payload, slack_team_obj: SlackInstallation):
        """Fires when the owner clicks the configuration button in App Home"""
        # Slack wraps actions in a list [1]
        actions = payload.get("actions", [])
        action = actions[0]
        action_id = action.get("action_id")

        user = payload.get("user", {})
        user_id = user.get("id", None)
        if not actions:
            return HttpResponse(status=200)

        if action_id == 'app_home_submit_settings' or action_id == 'jira_tag_extraction_source_input':
            _parse_bot_admins(payload, slack_team_obj)
            _parse_atlassian_subnet(payload, slack_team_obj)
            _parse_jira_token(payload, slack_team_obj)

            slack_team_obj.save()
            SlackEventSubscriptions.publish_app_home(user_id, slack_team_obj)
        else:
            return HttpResponse(f"unsupported action_id {action_id}", status=400)

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

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackInteractivityView.")

    def put(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PUT SlackInteractivityView.")

    def get(self, request):
        log_request_data(request)
        return HttpResponse("GET SlackInteractivityView.")
