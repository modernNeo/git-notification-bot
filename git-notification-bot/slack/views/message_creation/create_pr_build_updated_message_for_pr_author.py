from slack.views.message_creation.utilities import get_slack_id_by_atlassian_account_id, create_commit_footer_link


def create_pr_build_updated_message_for_pr_author(author_atlassian_id: str, build_status: bool,
                                                  abbreviated_commit_hash: str, commit_message: str, commit_link: str,
                                                  build_status_link: str, test_name: str):
    author_slack_id = get_slack_id_by_atlassian_account_id(author_atlassian_id)
    return {
        "channel": author_slack_id,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Commit Build {'Passed :white_check_mark:' if build_status else 'Failed :x:'}"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{author_slack_id}>,\n\n"
                        f'<{build_status_link}|Test "{test_name}" {'passed' if build_status else 'failed'}> on your '
                        f'commit <{commit_link}|{abbreviated_commit_hash}>'
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
            "text": create_commit_footer_link(commit_message, commit_link)
        }]
    }
