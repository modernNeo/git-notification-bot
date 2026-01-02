from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_pr_footer_link


def create_pr_approved_message_for_pr_author(author_atlassian_id: str, atlassian_id_for_person_who_approved_pr: str,
                                             pr_title: str, pr_description, pr_link: str):
    author_slack_id = get_slack_id_by_atlassian_account_id(author_atlassian_id)
    return {
        "channel": author_slack_id,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "PR Approved :white_check_mark:"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{author_slack_id}>,\n\n"
                        f"<@{get_slack_id_by_atlassian_account_id(atlassian_id_for_person_who_approved_pr)}> "
                        f"approved your PR <{pr_link}|{pr_title}>"
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