from django.urls import path

from slack.views.slack_callback_view import SlackCallbackView
from slack.views.slack_install_view import SlackInstallView

urlpatterns = [
    path('', SlackCallbackView.as_view(), name='slack_callback'),  # Your root redirect endpoint
    path('install', SlackInstallView.as_view(), name='slack_install'),
]
