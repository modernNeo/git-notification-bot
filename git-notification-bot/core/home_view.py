import json

from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"

    def log_request_data(self, request):
        """Helper method to print incoming request details."""
        print(f"\n--- Incoming {request.method} Request ---")
        print("Path:", request.path)
        print("Query Params (GET):", dict(request.GET))
        print("Headers:", dict(request.headers))

        # Read JSON body for POST/PATCH if content-type is JSON
        if request.content_type == "application/json":
            try:
                print("Body (JSON):", json.loads(request.body))
            except json.JSONDecodeError:
                print("Body (Invalid JSON):", request.body)
        else:
            print("Form Data (POST):", dict(request.POST))

    def get(self, request, *args, **kwargs):
        self.log_request_data(request)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        self.log_request_data(request)
        # Process POST data here
        return render(request, self.template_name)

    def patch(self, request, *args, **kwargs):
        self.log_request_data(request)
        # Process PATCH data here
        return render(request, self.template_name)
