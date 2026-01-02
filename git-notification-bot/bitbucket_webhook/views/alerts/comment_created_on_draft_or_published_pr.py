import re

from django.http import HttpResponse

from atlassian.views.Constants import Constants
from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_message_for_pr_comment_for_mentioned_user import \
    create_message_for_pr_comment_for_mentioned_user
from slack.views.message_creation.create_message_for_pr_comment_for_pr_author import \
    create_message_for_pr_comment_for_pr_author


def process(payload):
    messages = []
    author_atlassian_id = payload['pullrequest']['author']['account_id']
    comment_info = payload['comment']
    comment = comment_info['content']['raw']
    comment_author_account_id = comment_info['user']['account_id']
    parent_comment_id = comment_info['id']
    pr_title = payload['pullrequest']['title']
    pr_link = payload['pullrequest']['links']['html']['href']
    comment_link = payload['comment']['links']['html']['href']
    pr_description = payload['pullrequest']['description']
    atlassian_ids_for_people_to_alert = []
    matched_ids_results = re.search(Constants.REGEX_ATLASSIAN_ACCOUNT_ID, comment)

    if matched_ids_results:
        for matched_id in matched_ids_results.groups():
            if matched_id != author_atlassian_id:
                atlassian_ids_for_people_to_alert.append(matched_id)

    messages.append(
        create_message_for_pr_comment_for_pr_author(author_atlassian_id, comment_author_account_id, comment, pr_title,
                                                    pr_description, pr_link, comment_link)
    )
    for atlassian_id_for_person_to_alert in atlassian_ids_for_people_to_alert:
        messages.append(create_message_for_pr_comment_for_mentioned_user(atlassian_id_for_person_to_alert,
                                                                         comment_author_account_id, author_atlassian_id,
                                                                         comment, pr_title, pr_description, pr_link,
                                                                         comment_link))
    return MessagesToSend(
        messages,
        HttpResponse(f"Successfully processed action for comment on PR.")
    )