import secrets

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from core.log_request_data import log_request_data

# Keep these secrets inside your settings.py environment variables!
SCOPES = "chat:write,commands"


class SlackInstallView(View):
    """Generates the secure state and redirects the user to Slack."""

    def get(self, request):
        log_request_data(request)
        # 1. Generate unique state token
        state_token = secrets.token_hex(16)

        # 2. Save token inside Django's session engine
        request.session["oauth_state"] = state_token

        # 3. Direct to Slack authorization url
        slack_url = (
            f"https://slack.com"
            f"?client_id={settings.SLACK_CLIENT_ID}"
            f"&scope={SCOPES}"
            f"&redirect_uri={settings.ALLOWED_HOSTS[0] + "/slack"}"
            f"&state={state_token}"
        )
        return redirect(slack_url)

    def post(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("POST SlackInstallView.")

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackInstallView.")
