from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_comment_string, \
    create_pr_footer_link


def create_message_for_pr_comment_for_mentioned_user(atlassian_id_for_person_to_alert: str,
                                                     comment_author_account_id: str, author_atlassian_id: str,
                                                     comment: str, pr_title: str, pr_description, pr_link: str,
                                                     comment_link: str):
    get_slack_id_for_person_to_alert = get_slack_id_by_atlassian_account_id(atlassian_id_for_person_to_alert)
    return {
        "channel": get_slack_id_for_person_to_alert,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Comment made on PR :writing_hand:"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{get_slack_id_for_person_to_alert}>,\n\n"
                        f"<@{get_slack_id_by_atlassian_account_id(comment_author_account_id)}> left the following "
                        f"<{comment_link}|comment> on <@{get_slack_id_by_atlassian_account_id(author_atlassian_id)}"
                        f">'s PR <{pr_link}|{pr_title}>"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Done"
                },
                "style": "primary",
                "value": "click_me_456"
            }
        }, {
            "type": "divider"
        }, {
            "type": "markdown",
            "text": create_comment_string(comment)
        }, {
            "type": "divider"
        }, {
            "type": "markdown",
            "text": create_pr_footer_link(pr_title, pr_description, pr_link)
        }]
    }