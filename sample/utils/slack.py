# -*- coding:utf-8 -*-

from __future__ import absolute_import

import logging
import socket

from django.conf import settings
from slacker import Slacker

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


class SlackerWrapper(object):
    def __init__(self, channel=settings.SLACK_BOT_CHANNEL, username=settings.SLACK_BOT_USERNAME):
        self.slack_client = Slacker(getattr(settings, 'SLACK_BOT_TOKEN', ''))
        self.channel = channel
        self.username = username

    def post_message(self, message, attachments=None):
        if not settings.TESTING:
            try:
                self.slack_client.chat.post_message(
                    self.channel,
                    ''.join([message, ' worked on %s.' % socket.gethostname()]),
                    username=self.username,
                    attachments=attachments
                )
            except Exception as e:
                logger.error('cannot post into slack.\terror:%s', str(e))
