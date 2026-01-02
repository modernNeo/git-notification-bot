import hashlib
import hmac
import json

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse

from bitbucket_webhook.views.alerts.build_status_updated import process as build_status_updated
from bitbucket_webhook.views.alerts.changes_requested_on_pr import process as changes_requested_on_pr
from bitbucket_webhook.views.alerts.comment_created_on_draft_or_published_pr import process as \
    comment_created_on_draft_or_published_pr
from bitbucket_webhook.views.alerts.draft_pr_published_with_request_reviewers import \
    process as draft_pr_published_with_request_reviewers
from bitbucket_webhook.views.alerts.pr_approved import process as pr_approved
from bitbucket_webhook.views.alerts.pr_create_and_published_at_same_time_with_request_reviewers import \
    process as pr_create_and_published_at_same_time_with_request_reviewers
from bitbucket_webhook.views.alerts.pr_created_and_published_with_no_requested_reviewers import \
    process as pr_created_and_published_with_no_requested_reviewers
from bitbucket_webhook.views.messages_to_send import MessagesToSend


def payload_processor(request) -> MessagesToSend:
    _verify_request(request)
    event_key = request.headers['X-Event-Key']
    number_of_reviewers = None
    no_reviewers = None
    reviewers_requested = None
    draft_pr = None
    published_pr = None
    if 'pullrequest' in request.data:
        number_of_reviewers = len(request.data['pullrequest']['reviewers'])
        no_reviewers = len(request.data['pullrequest']['reviewers']) == 0
        reviewers_requested = not no_reviewers
        draft_pr = request.data['pullrequest']['draft']
        published_pr = not draft_pr
    if event_key == 'pullrequest:created':
        if published_pr:
            if no_reviewers:
                return pr_created_and_published_with_no_requested_reviewers(request.data)
            elif reviewers_requested and published_pr:
                return pr_create_and_published_at_same_time_with_request_reviewers(request.data)
        else:
            return MessagesToSend(
                [],
                HttpResponse(f"Skipping processing for draft PR.")
            )
    if event_key == 'pullrequest:updated':
        if published_pr and no_reviewers:
            return pr_created_and_published_with_no_requested_reviewers(request.data)
        if published_pr and reviewers_requested:
            return draft_pr_published_with_request_reviewers(request.data)
        elif draft_pr:
            return MessagesToSend(
                [],
                HttpResponse(f"Skipping processing for draft PR.")
            )
    elif event_key == "pullrequest:comment_created":
        return comment_created_on_draft_or_published_pr(request.data)
    elif event_key == 'pullrequest:changes_request_created':
        return changes_requested_on_pr(request.data)
    elif event_key == 'pullrequest:approved':
        return pr_approved(request.data)
    elif event_key == 'repo:commit_status_updated':
        return build_status_updated(request.data)
    return MessagesToSend(
        [],
        HttpResponseBadRequest(
            f"Bot does not support event {event_key} on a payload with "
            f"{'no reviewers' if no_reviewers else f'{number_of_reviewers} reviewer[s]'} from a "
            f"{'Draft PR' if draft_pr else 'Published PR'} ")
    )


def _verify_request(request):
    if settings.BITBUCKET_SECRET is None:
        return
    modified_payload = json.dumps(request.data, separators=(',', ':'), ensure_ascii=False)
    hash_object = hmac.new(
        settings.BITBUCKET_SECRET.encode("utf-8"),
        msg=modified_payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    )
    calculated_signature = "sha256=" + hash_object.hexdigest()
    given_signature = request.headers['X-Hub-Signature']
    if not hmac.compare_digest(calculated_signature, given_signature):
        raise Exception(
            "Signatures do not match\nExpected signature:"
            f" {calculated_signature}\nActual: signature: {given_signature}"
        )
