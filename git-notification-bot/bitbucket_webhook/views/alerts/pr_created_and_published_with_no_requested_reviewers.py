from django.http import HttpResponse

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_message_for_pr_author import create_message_for_pr_author


def process(payload):
    author_atlassian_id = payload['pullrequest']['author']['account_id']
    pr_title = payload['pullrequest']['title']
    pr_description = payload['pullrequest']['description']
    pr_link = payload['pullrequest']['links']['html']['href']
    return MessagesToSend(
        [create_message_for_pr_author(author_atlassian_id, pr_title, pr_description, pr_link)],
        HttpResponse(f"Successfully processed action for PR published with no reviewers.")
    )