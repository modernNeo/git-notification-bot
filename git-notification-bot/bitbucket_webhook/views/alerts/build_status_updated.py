from django.http import HttpResponse

from bitbucket_webhook.views.messages_to_send import MessagesToSend
from slack.views.message_creation.create_pr_build_updated_message_for_pr_author import \
    create_pr_build_updated_message_for_pr_author


def process(payload):
    commit_status = payload['commit_status']
    build_status = commit_status['state'] == 'SUCCESSFUL'
    build_status_link = commit_status['url']
    test_name = commit_status['name']

    commit = commit_status['commit']
    pr_author_atlassian_id = commit['author']['user']['account_id']
    commit_message = commit['message'].replace("\n", "")
    commit_link = commit['links']['html']['href']
    abbreviated_commit_hash = commit['hash'][:7]

    return MessagesToSend(
        [
            create_pr_build_updated_message_for_pr_author(
                pr_author_atlassian_id, build_status, abbreviated_commit_hash, commit_message, commit_link,
                build_status_link, test_name
            )
        ],
        HttpResponse(f"Successfully processed action for update in build status.")
    )
