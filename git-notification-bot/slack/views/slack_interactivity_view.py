import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.log_request_data import log_request_data
from slack.models import SlackInstallation, BotWorkspaceAdmin
from slack.views.bot_workspace_admin_queries import attempt_slack_query_for_workspace_owners, get_custom_bot_admins
from slack.views.slack_event_subscriptions import SlackEventSubscriptions


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

        if action_id == 'app_home_submit_settings':
            view = payload.get("view", {})
            state = view.get("state", {})
            values = state.get("values", {})
            git_notification_bot_admins_block = values.get("git_notification_bot_admins_block", {})
            git_notification_bot_admins = git_notification_bot_admins_block.get("git_notification_bot_admins", {})

            workspace_owners = attempt_slack_query_for_workspace_owners(slack_team_obj)
            selected_users = git_notification_bot_admins.get("selected_users", [])
            selected_users = [
                selected_user
                for selected_user in selected_users
                if selected_user not in workspace_owners
            ]

            current_admins_user_ids = list(get_custom_bot_admins(slack_team_obj))

            new_users_ids = [
                user_id for user_id in selected_users
                if user_id not in current_admins_user_ids
            ]
            new_admins = [
                BotWorkspaceAdmin(user_id=selected_users_id, workspace=slack_team_obj)
                for selected_users_id in new_users_ids
            ]

            users_to_delete = [
                current_admin
                for current_admin in current_admins_user_ids
                if current_admin not in selected_users
            ]

            if len(new_admins) > 0:
                message = " ".join([f"saved {admin}\n" for admin in new_admins])
                print(f"{message}")
                BotWorkspaceAdmin.objects.bulk_create(new_admins, ignore_conflicts=True)
            deleted_admins = BotWorkspaceAdmin.objects.filter(user_id__in=users_to_delete)
            if len(deleted_admins) > 0:
                message = " ".join([f"deleted {admin}\n" for admin in deleted_admins])
                print(f"{message}")
                deleted_admins.delete()
            SlackEventSubscriptions.publish_app_home(user_id, slack_team_obj)
        else:
            return HttpResponse("unsupported action_id", status=400)

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
