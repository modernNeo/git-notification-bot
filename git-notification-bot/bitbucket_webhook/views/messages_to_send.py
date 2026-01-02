from typing import List

from django.http import HttpResponse


class MessageToSend:

    def __int__(self, channel_id : str, blocks : List[dict]):
        self.channel_id = channel_id
        self.blocks : List[dict] = blocks

class MessagesToSend:

    def __init__(self, message_to_send: List[MessageToSend], api_response : HttpResponse):
        self.messages_to_send: List[MessageToSend] = message_to_send
        self.api_response = api_response

