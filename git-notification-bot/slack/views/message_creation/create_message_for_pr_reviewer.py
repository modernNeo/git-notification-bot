from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_pr_footer_link


def create_message_for_pr_reviewer(author_atlassian_id: str, pr_reviewer_atlassian_id: str, pr_title: str,
                                   pr_description, pr_link: str):
    reviewer_slack_id = get_slack_id_by_atlassian_account_id(pr_reviewer_atlassian_id)
    author_slack_id = get_slack_id_by_atlassian_account_id(author_atlassian_id)
    return {
        "channel": reviewer_slack_id,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Review Requested"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{reviewer_slack_id}>!\n\n<@{author_slack_id}> is asking for your review on their PR "
                        f"<{pr_link}|{pr_title}>"
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
            "text": create_pr_footer_link(pr_title, pr_description, pr_link)
        }]
    }
