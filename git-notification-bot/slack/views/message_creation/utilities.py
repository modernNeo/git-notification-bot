import re

from django.conf import settings

from atlassian.views.Constants import Constants
from atlassian.views.get_account_info import get_account_info
from atlassian.views.get_ticket_title import get_ticket_title
from core.settings import JiraTagExtractionSource
from slack.views.lookup_by_email import lookup_user_id_by_email


def create_comment_string(comment: str) -> str:
    matched_ids_results = re.search(Constants.REGEX_ATLASSIAN_ACCOUNT_ID, comment)
    new_comment = comment
    if matched_ids_results:
        for matched_ids_result in matched_ids_results.groups():
            new_comment = new_comment.replace(
                f"@{{{matched_ids_result}}}",
                f"<@{get_slack_id_by_atlassian_account_id(matched_ids_result)}>"
            )
    return new_comment


def get_slack_id_by_atlassian_account_id(pr_reviewer_atlassian_id: str) -> str | None:
    return lookup_user_id_by_email(get_account_info(pr_reviewer_atlassian_id))


def create_pr_footer_link(pr_title: str, pr_description: str, pr_link: str) -> str:
    footer = f"Bitbucket PR Link: <{pr_link}|{pr_title}>\n"
    jira_tag = _extract_jira_tag(
        pr_title if settings.JIRA_TAG_EXTRACTION_SOURCE == JiraTagExtractionSource.TITLE else pr_description)
    ticket_title = get_ticket_title(jira_tag)
    if ticket_title and settings.ATLASSIAN_SUBNET and jira_tag:
        footer += (f"Jira Link: <https://{settings.ATLASSIAN_SUBNET}.atlassian.net/browse/{jira_tag}|{jira_tag}: "
                   f"{ticket_title}>")
    return footer


def create_commit_footer_link(commit_message: str, commit_link: str) -> str:
    footer = f"Bitbucket Commit Link: <{commit_link}|{commit_message}>\n"
    jira_tag = _extract_jira_tag(commit_message)
    ticket_title = get_ticket_title(jira_tag)
    if ticket_title and settings.ATLASSIAN_SUBNET and jira_tag:
        footer += (f"Jira Link: <https://{settings.ATLASSIAN_SUBNET}.atlassian.net/browse/{jira_tag}|{jira_tag}: "
                   f"{ticket_title}>")
    return footer


def _extract_jira_tag(title: str) -> None | str:
    if settings.JRA_TAG_PATTERN_MATCHER is None:
        return None
    results = re.search(settings.JRA_TAG_PATTERN_MATCHER, title)
    if results is None:
        return None
    return results.group()[1:-2]
