from django.http import HttpResponse

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_message_for_pr_reviewer import create_message_for_pr_reviewer


def process(payload):
    messages = []
    author_atlassian_id = payload['pullrequest']['author']['account_id']
    pr_title = payload['pullrequest']['title']
    pr_link = payload['pullrequest']['links']['html']['href']
    pr_description = payload['pullrequest']['description']
    for reviewer in payload['pullrequest']['reviewers']:
        requested_reviewer_atlassian_id = reviewer['account_id']
        messages.append(
            create_message_for_pr_reviewer(author_atlassian_id, requested_reviewer_atlassian_id, pr_title, pr_description,
                                           pr_link)
        )
    return MessagesToSend(
        messages,
        HttpResponse(f"Successfully processed action for PR published with reviewers.")
    )
