import json
import logging

from django.conf import settings
from django.core.mail import mail_admins
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework.permissions import AllowAny

from users.models import User

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


@method_decorator(csrf_exempt, name='dispatch')
class MailUndelivered(View):
    """
    Receive and process AWS SNS notification.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Validate notifications is coming from AWS SES.
        if not self._validate_headers():
            raise Http404()

        try:
            data = json.loads(request.body.decode('utf-8')) if isinstance(request.body.decode('utf-8'),
                                                                          str) else request.body.decode('utf-8')
        except ValueError:
            logger.error('request body is not json format.\tmessage:{}'.format(request.body.decode('utf-8')))
            raise Http404()

        if data.get('Type') == 'SubscriptionConfirmation':
            subscribe_url = data.get('SubscribeURL')
            subscribe_body = "Visit this url to confirm subscription to AWS SNS\n\n{}".format(subscribe_url)
            mail_admins('SNS subscription confirmation', subscribe_body)
            return HttpResponse()

        try:
            message = json.loads(data.get('Message')) if isinstance(data.get('Message'), str) else data.get('Message')
        except ValueError:
            logger.error('Message field is not json format.\tmessage:{}'.format(data.get('message')))
            raise Http404()

        emails = message.get('mail').get('destination')
        if emails:
            User.objects.filter(email__in=emails).update(is_mail_unreachable=True)
            logger.info('Email addresses marked as unreachable: {}'.format(','.join(emails)))
        else:
            logger.error('The "destination" field is empty.\tmessage:{}'.format(message))
            raise Http404()
        return HttpResponse()

    def _validate_headers(self):
        """
        Validates that request is coming from AWS SNS.
        :return: True if request is comes from AWS SNS, False otherwise
        """
        if self.request.META.get('HTTP_X_AMZ_SNS_TOPIC_ARN') != settings.SNS_TOPIC_ARN:
            logger.error("HTTP_X_AMZ_SNS_TOPIC_ARN header doesn't match.\tvalue:%s",
                         self.request.META.get('HTTP_X_AMZ_SNS_TOPIC_ARN'))
            return False
        return True
