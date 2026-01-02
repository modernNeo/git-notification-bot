import json

from rest_framework import views

from bitbucket_webhook.views.payload_processor import payload_processor
from python_logging.setup_logger import Loggers

logger = Loggers.get_logger(logger_name="bitbucket_logging")[0]

class BitbucketWebhook(views.APIView):

    def post(self, request):
        logger.info(request)
        logger.info(json.dumps({**request.headers}, indent=4))
        logger.info(json.dumps(request.data, indent=4))
        messages = payload_processor(request)
        return messages