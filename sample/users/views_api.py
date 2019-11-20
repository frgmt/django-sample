import logging
import re

from django.conf import settings
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from utils.errors_api import AE106, AE107, AE109, AE110, AE111, AE112

from users.models import (
    User, MINIMUM_PASSWORD_LENGTH, MINIMUM_USERNAME_LENGTH
)

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


def get_or_create_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_201_CREATED if getattr(user, 'is_new', False) else HTTP_200_OK)


def validate_user_data(username=None, password=None, email=None):
    """ the reason of validating user data in view other than serializer is that
    RegisterUser doesn't use serializer at all.
    :param username:
    :param password:
    :param email:
    """
    if username:
        # either username or nickname is already taken?
        if User.objects.filter(Q(username=username) | Q(nickname=username)).exists():
            raise AE106()
        # username is too long?
        # noinspection PyProtectedMember
        if len(username) > User._meta.get_field('username').max_length:
            raise AE109()
        # or too short?
        if len(username) < MINIMUM_USERNAME_LENGTH:
            raise AE111()
        # or invalid? (keep the regexp up to date with the the one used in UserForm.)
        if not re.match(r"(^[0-9A-Z]+([-_0-9A-Z]+)*$)", username, re.IGNORECASE):
            raise AE112()

    if email:
        # email is already taken?
        if User.objects.filter(email=email, is_active=True).exists():
            raise AE107()
    if password:
        # password is too short?
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            raise AE110()
