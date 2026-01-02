from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_pr_footer_link


def create_message_for_pr_author(author_atlassian_id: str, pr_title: str, pr_description: str, pr_link: str):
    author_slack_id = get_slack_id_by_atlassian_account_id(author_atlassian_id)
    return {
        "channel": author_slack_id,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "No Reviewer Detected on PR"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{author_slack_id}>!\n\nDon't forget to assign a reviewer to your PR <{pr_link}|"
                        f"{pr_title}>"
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