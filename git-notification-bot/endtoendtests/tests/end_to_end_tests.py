import re

from django.test import TestCase

from bitbucket_webhook.views.payload_processor import payload_processor
from endtoendtests.tests.BitbucketRequest import BitbucketRequest
from endtoendtests.tests.send_messages import send_messages

# Create your tests here

SEND_SLACK_MESSAGES = True


class EndtoEndTests(TestCase):

    def test_pr_create_and_published_at_same_time_with_no_request_reviewers(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_1.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "No Reviewer Detected on PR"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hi <@U0A70PHBALQ>!\n\nDon't forget to assign a reviewer to your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/15|[NGA-121] PR Title>"
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
                    "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/15|[NGA-121] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-121|NGA-121: FE - Add icons to the tree>'
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_draft_pr_published_with_no_request_reviewers(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_4.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "No Reviewer Detected on PR"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hi <@U0A70PHBALQ>!\n\nDon't forget to assign a reviewer to your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/16|[NGA-124] PR Title>"
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
                    "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/16|[NGA-124] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-124|NGA-124: BE - Datagap - create a dataGap database>'
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_pr_create_and_published_at_same_time_with_request_reviewers(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_2.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [{
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Review Requested"
                    }
                },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A5ZM1F8PN>!\n\n<@U0A70PHBALQ> is asking for your review on their PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/17|[NGA-122] PR Title>'
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
                    "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/17|[NGA-122] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-122|NGA-122: FE - Add paging to the tree>'
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_draft_pr_published_with_request_reviewers(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_5.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Review Requested"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A5ZM1F8PN>!\n\n<@U0A70PHBALQ> is asking for your review on their PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/18|[NGA-125] PR Title>'
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
                    "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/18|[NGA-125] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-125|NGA-125: BE - Datagap - update database with data-receipt summary message>'
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_pr_created_in_draft_mode(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_3.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        self.assertEqual(len(messages_to_send.messages_to_send), 0)

    def test_published_pr_moved_to_draft_mode(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_6.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        self.assertEqual(len(messages_to_send.messages_to_send), 0)

    def test_inline_comment_made_on_new_thread(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_7.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for index, message_to_send in enumerate(messages_to_send.messages_to_send):
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            if index == 0:
                self.assertEqual(
                    message_to_send['blocks'],
                    [{
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Comment made on PR :writing_hand:"
                        }
                    },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21/_/diff#comment-732824753|comment> on your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21|[NGA-127] PR Title>'
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'line 4 <@U0A692TLQBT>  inline comment'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21|[NGA-127] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-127|NGA-127: BE- Datagap - update config for benefit of gap-monitor>'
                        }
                    ],
                    "Unexpected block structure"
                )
            else:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hi <@U0A692TLQBT>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21/_/diff#comment-732824753|comment> on <@U0A70PHBALQ>'s PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21|[NGA-127] PR Title>"
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'line 4 <@U0A692TLQBT>  inline comment'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/21|[NGA-127] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-127|NGA-127: BE- Datagap - update config for benefit of gap-monitor>'
                        }
                    ],
                    "Unexpected block structure"
                )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_reply_inline_comment_made_on_existing_thread(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_10.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for index, message_to_send in enumerate(messages_to_send.messages_to_send):
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            if index == 0:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22/_/diff#comment-732825004|comment> on your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22|[NGA-1210] PR Title>'
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'actually <@U0A70PHBALQ> , maybe not?'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22|[NGA-1210] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1210|NGA-1210: BE - Dataloader - replace Ameren with AmerenIllinois in tenant and processor naming>'
                        }
                    ],
                    "Unexpected block structure"
                )
            else:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22/_/diff#comment-732825004|comment> on <@U0A70PHBALQ>'s PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22|[NGA-1210] PR Title>"
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'actually <@U0A70PHBALQ> , maybe not?'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/22|[NGA-1210] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1210|NGA-1210: BE - Dataloader - replace Ameren with AmerenIllinois in tenant and processor naming>'
                        }
                    ],
                    "Unexpected block structure"
                )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_overview_comment_made_on_new_thread(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_15.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for index, message_to_send in enumerate(messages_to_send.messages_to_send):
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            if index == 0:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23/_/diff#comment-732825663|comment> on your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23|[NGA-1215] PR Title>'
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'overview <@U0A692TLQBT> comment.'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23|[NGA-1215] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1215|NGA-1215: FE - Implement new login page image and app name>'
                        }
                    ],
                    "Unexpected block structure"
                )
            else:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hi <@U0A692TLQBT>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23/_/diff#comment-732825663|comment> on <@U0A70PHBALQ>'s PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23|[NGA-1215] PR Title>"
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'overview <@U0A692TLQBT> comment.'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/23|[NGA-1215] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1215|NGA-1215: FE - Implement new login page image and app name>'
                        }
                    ],
                    "Unexpected block structure"
                )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_overview_comment_made_on_existing_thread(self):
        pr_published_with_no_reviewers = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_18.json")
        messages_to_send = payload_processor(pr_published_with_no_reviewers)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for index, message_to_send in enumerate(messages_to_send.messages_to_send):
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            if index == 0:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24/_/diff#comment-732825850|comment> on your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24|[NGA-1218] PR Title>'
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'actually, <@U0A70PHBALQ> maybe not?'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24|[NGA-1218] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1218|NGA-1218: BE - Create new "Data Count" endpoint>'
                        }
                    ],
                    "Unexpected block structure"
                )
            else:
                self.assertEqual(
                    message_to_send['blocks'],
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Comment made on PR :writing_hand:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> left the following <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24/_/diff#comment-732825850|comment> on <@U0A70PHBALQ>'s PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24|[NGA-1218] PR Title>"
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
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'actually, <@U0A70PHBALQ> maybe not?'
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "markdown",
                            "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/24|[NGA-1218] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1218|NGA-1218: BE - Create new "Data Count" endpoint>'
                        }
                    ],
                    "Unexpected block structure"
                )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_changed_requested_on_pr(self):
        pr_approved = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_23.json")
        messages_to_send = payload_processor(pr_approved)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Change Requested on PR :x:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> request changes on your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/25|[NGA-1223] PR Title>'
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
                    "text": "Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/25|[NGA-1223] PR Title>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1223|NGA-1223: BE - Login with user created on Group nodetype gives error node's out of scope>"
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_approval_on_pr(self):
        pr_approved = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_24.json")
        messages_to_send = payload_processor(pr_approved)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "PR Approved :white_check_mark:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A70PHBALQ>,\n\n<@U0A5ZM1F8PN> approved your PR <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/26|[NGA-1224] PR Title>'
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
                    "text": 'Bitbucket PR Link: <https://bitbucket.org/git_slack_pr_bot/test/pull-requests/26|[NGA-1224] PR Title>'
                            '\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1224|NGA-1224: BE - Many GET  and DELETE endpoints in Node service erroneously ask for a Content-Type header>'
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_build_passed_on_pr(self):
        pr_approved = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_26.json")
        messages_to_send = payload_processor(pr_approved)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Commit Build Passed :white_check_mark:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A70PHBALQ>,\n\n<https://bitbucket.org/git_slack_pr_bot/test/pipelines/results/5|Test "Pipeline - default" passed> on your commit <https://bitbucket.org/git_slack_pr_bot/test/commits/0344c85f41f031f003fdd9195d96235f0aaba542|0344c85>'
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
                    "text": "Bitbucket Commit Link: <https://bitbucket.org/git_slack_pr_bot/test/commits/0344c85f41f031f003fdd9195d96235f0aaba542|[NGA-1226] adding test>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1226|NGA-1226: FE - Update automation scripts as per changes in 1212>"
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)

    def test_build_failed_on_pr(self):
        pr_approved = BitbucketRequest("endtoendtests/tests/bitbucket_payloads/case_28.json")
        messages_to_send = payload_processor(pr_approved)
        self.assertEqual(messages_to_send.api_response.status_code, 200, messages_to_send.api_response.text)
        for message_to_send in messages_to_send.messages_to_send:
            self.assertIsNotNone(re.match(r"^\w{11}$", message_to_send['channel']), "invalid channel id specified")
            self.assertEqual(
                message_to_send['blocks'],
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Commit Build Failed :x:"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Hi <@U0A70PHBALQ>,\n\n<https://bitbucket.org/git_slack_pr_bot/test/pipelines/results/6|Test "Pipeline - default" failed> on your commit <https://bitbucket.org/git_slack_pr_bot/test/commits/8cfe3f4b371dd6eecb2ec73261f15ab39072cd72|8cfe3f4>'
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
                    "text": "Bitbucket Commit Link: <https://bitbucket.org/git_slack_pr_bot/test/commits/8cfe3f4b371dd6eecb2ec73261f15ab39072cd72|[NGA-1228] adding test>\nJira Link: <https://powertakeoff.atlassian.net/browse/NGA-1228|NGA-1228: FE - Sub Side Navigation menu items should be highlighted on mouse hover>"
                }
                ],
                "Unexpected block structure"
            )
        if SEND_SLACK_MESSAGES:
            send_messages(messages_to_send)
