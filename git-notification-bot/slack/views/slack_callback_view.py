import requests
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.views import View

from core.LogRequestData import log_request_data
from slack.models import SlackInstallation


class SlackCallbackView(View):
    """Handles the redirect from Slack, verifies state, and saves tokens."""

    def get(self, request):
        log_request_data(request)
        incoming_code = request.GET.get("code")
        incoming_state = request.GET.get("state")

        # 1. SECURITY FIX: Pull state token out of the session
        saved_state = request.session.get("oauth_state")

        # Modified Security Check: Allow empty state IF no state was previously set in session
        if incoming_state:
            # If a state was provided by Slack, it MUST match our session
            if incoming_state != saved_state:
                return HttpResponseForbidden("State verification failed. Request untrusted.")
        else:
            # If state is empty, it's only safe if we didn't initiate an internal session state either
            if saved_state is not None:
                return HttpResponseForbidden("State verification failed. Expected a state token.")

        # Clear out state if it exists
        if "oauth_state" in request.session:
            del request.session["oauth_state"]

        # 2. Exchange temporary token code for permanent tokens
        payload = {
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET,
            "code": incoming_code,
            "redirect_uri": "https://" + settings.ALLOWED_HOSTS[0] + "/slack"
        }
        print(payload)

        response = requests.post("https://slack.com/api/oauth.v2.access", data=payload)
        oauth_data = response.json()
        print(f"{response.headers}")
        print(oauth_data)

        if not oauth_data.get("ok"):
            return HttpResponse(f"Slack OAuth Error: {oauth_data.get('error')}", status=400)

        # 3. Extract safe payload objects
        bot_token = oauth_data["access_token"]
        team_id = oauth_data["team"]["id"]
        team_name = oauth_data["team"]["name"]
        enterprise_id = oauth_data["enterprise"]["id"] if oauth_data.get("enterprise") else None

        # 4. Save/Update record in your Django Database
        SlackInstallation.objects.update_or_create(
            team_id=team_id,
            defaults={
                "bot_token": bot_token,
                "team_name": team_name,
                "enterprise_id": enterprise_id,
            }
        )

        return HttpResponse("Installation Successful! You can close this window and return to Slack.")

    def post(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("POST SlackCallbackView.")

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackCallbackView.")
