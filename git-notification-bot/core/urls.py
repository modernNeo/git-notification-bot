"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core.home_view import HomeView
from slack.views.slack_callback_view import SlackCallbackView
from slack.views.slack_install_view import SlackInstallView

urlpatterns = [

    path('slack/install/', SlackInstallView.as_view(), name='slack_install'),
    path('slack', SlackCallbackView.as_view(), name='slack_callback'),  # Your root redirect endpoint
    path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    path('bitbucket/', include('bitbucket_webhook.urls'))
]
