import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from core.LogRequestData import log_request_data
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")  # 3. Apply the exemption
class SlackEventSubscriptions(View):
    """Generates the secure state and redirects the user to Slack."""

    def get(self, request):
        log_request_data(request)
        return HttpResponse("GET SlackEventSubscriptions.")

    def post(self, request, *args, **kwargs):
        log_request_data(request)

        # Parse Slack's JSON payload
        try:
            data = json.loads(request.body.decode("utf-8"))

            # If Slack is testing the URL, return the challenge parameter
            if data.get("type") == "url_verification":
                return HttpResponse(data.get("challenge"), content_type="text/plain")

        except json.JSONDecodeError:
            pass

        return HttpResponse("POST SlackEventSubscriptions.")

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackEventSubscriptions.")

    def put(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PUT SlackEventSubscriptions.")
