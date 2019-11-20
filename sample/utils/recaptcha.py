# -*- coding:utf-8 -*-

import requests
from django.conf import settings

RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'


class Recaptcha(object):
    """
    ret value is bellow dict

    { "success": true|false,
      "error-codes": [...]   // optional
    }

    see: https://developers.google.com/recaptcha/docs/verify
    """
    @staticmethod
    def verify(g_recaptcha_res):
        url = "{0}?secret={1}&response={2}".format(RECAPTCHA_URL, settings.GOOGLE_RECAPTCHA, g_recaptcha_res)
        return requests.get(url).json()
