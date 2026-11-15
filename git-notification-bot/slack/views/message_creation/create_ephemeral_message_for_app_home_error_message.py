def create_ephemeral_message_for_app_home_error_message(user_id, error_message: str):
    return {
        "channel": user_id,
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "App Home Input Error :x:"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hi <@{user_id}>,\n\n"
                        f'<{error_message}'
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
        }]
    }
