from django.shortcuts import render
from django.views.generic import TemplateView

from core.log_request_data import log_request_data


class HomeView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        log_request_data(request)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        log_request_data(request)
        # Process POST data here
        return render(request, self.template_name)

    def patch(self, request, *args, **kwargs):
        log_request_data(request)
        # Process PATCH data here
        return render(request, self.template_name)
