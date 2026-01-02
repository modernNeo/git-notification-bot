from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_comment_string, \
    create_pr_footer_link


def create_message_for_pr_comment_for_pr_author(author_atlassian_id: str, comment_author_account_id: str, comment: str,
                                                pr_title: str, pr_description, pr_link: str, comment_link: str):
    author_slack_id = get_slack_id_by_atlassian_account_id(author_atlassian_id)
    return {
        "channel": author_slack_id,
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
                "text": f"Hi <@{author_slack_id}>,\n\n"
                        f"<@{get_slack_id_by_atlassian_account_id(comment_author_account_id)}> left the following "
                        f"<{comment_link}|comment> on your PR <{pr_link}|{pr_title}>"
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
