from django.http import HttpResponse
from django.views import View

from core.LogRequestData import log_request_data


class SlackEventSubscriptions(View):
    """Generates the secure state and redirects the user to Slack."""

    def get(self, request):
        log_request_data(request)
        return HttpResponse("GET SlackEventSubscriptions.")

    def post(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("POST SlackEventSubscriptions.")

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PATCH SlackEventSubscriptions.")

    def put(self, request, *args, **kwargs):
        log_request_data(request)
        return HttpResponse("PUT SlackEventSubscriptions.")
