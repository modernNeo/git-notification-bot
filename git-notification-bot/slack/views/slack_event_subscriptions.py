import json

import requests
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.LogRequestData import log_request_data
from slack.models import SlackInstallation
from slack.views.include_custom_workspace_owners_for_initials_list import \
    include_custom_workspace_owners_for_initials_list


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
                self._publish_app_home(user_id, slack_team_obj)

        # Always return a 200 OK to acknowledge receipt of the event
        return HttpResponse(status=200)

    def _publish_app_home(self, user_id, slack_team_obj: SlackInstallation):
        """Pushes the initial Home Tab view containing your configuration button"""
        app_config_json = include_custom_workspace_owners_for_initials_list(
            json.load(open('slack/views/app_config.json', 'r', encoding='utf-8')), slack_team_obj)
        app_config_json['type'] = 'home'

        resp = requests.post(
            "https://slack.com/api/views.publish",
            headers={
                "Authorization": f"Bearer {slack_team_obj.bot_token}",
                "Content-Type": "application/json; charset=utf-8"
            },
            json={
                "user_id": user_id,
                "view": app_config_json
            }
        ).json()
        print(resp)

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackEventSubscriptions.")

    def put(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PUT SlackEventSubscriptions.")
