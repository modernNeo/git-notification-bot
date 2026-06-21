from django.urls import path

from slack.views.slack_callback_view import SlackCallbackView
from slack.views.slack_event_subscriptions import SlackEventSubscriptions
from slack.views.slack_install_view import SlackInstallView
from slack.views.slack_interactivity_view import SlackInteractivityView

urlpatterns = [
    path('', SlackCallbackView.as_view(), name='slack_callback'),  # Your root redirect endpoint
    path('install', SlackInstallView.as_view(), name='slack_install'),
    path('event_subscriptions', SlackEventSubscriptions.as_view(), name="event_subscriptions"),
    path("interactivity", SlackInteractivityView.as_view(), name="interactivity"),
]
