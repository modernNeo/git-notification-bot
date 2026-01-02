from django.urls import path

from bitbucket_webhook.views.bitbucket_webhook_api import BitbucketWebhook

urlpatterns = [path(r'', BitbucketWebhook.as_view())]
