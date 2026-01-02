from django.http import HttpResponse

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_changes_requested_message_for_pr_author import \
    create_changes_requested_message_for_pr_author


def process(payload):
    pr_author_atlassian_id = payload['pullrequest']['author']['account_id']
    atlassian_id_for_person_who_requested_changes = payload['changes_request']['user']['account_id']
    pr_title = payload['pullrequest']['title']
    pr_link = payload['pullrequest']['links']['html']['href']
    pr_description = payload['pullrequest']['description']
    return MessagesToSend(
        [create_changes_requested_message_for_pr_author(pr_author_atlassian_id,
                                                        atlassian_id_for_person_who_requested_changes, pr_title, pr_description,
                                                        pr_link)],
        HttpResponse(f"Successfully processed action for change requested on PR.")
    )