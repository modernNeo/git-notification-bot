from django.http import HttpResponse

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_pr_approved_message_for_pr_author import \
    create_pr_approved_message_for_pr_author


def process(payload):
    author_atlassian_id = payload['pullrequest']['author']['account_id']
    atlassian_id_for_person_who_approved_pr = payload['approval']['user']['account_id']

    pr_title = payload['pullrequest']['title']
    pr_link = payload['pullrequest']['links']['html']['href']
    pr_description = payload['pullrequest']['description']
    return MessagesToSend(
        [create_pr_approved_message_for_pr_author(author_atlassian_id, atlassian_id_for_person_who_approved_pr,
                                                  pr_title, pr_description, pr_link)],
        HttpResponse(f"Successfully processed action for approved PR.")
    )
