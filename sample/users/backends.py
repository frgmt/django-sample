# -*- coding:utf-8 -*-
import logging

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from rauth import OAuth1Session
from requests import RequestException

from utils import string
from utils.errors_api import AE107, AE108
from users import validators
from users.models import User

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))

GRAPH_API_URL = 'https://graph.facebook.com/v2.3'
TWITTER_API_URL = 'https://api.twitter.com/1.1'
INSTAGRAM_API_URL = 'https://api.instagram.com/v1'
LINE_API_URL = 'https://api.line.me/v2'


class MailLoginBackend(object):
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def authenticate(self, username=None, password=None, **kwargs):
        if not all((username, password)):  # lack of parameters.
            return None

        # checking is_active should be done in calling classes.
        user_queryset = User.objects.filter(email=username)
        try:
            user = user_queryset.get()
        except User.DoesNotExist:  # user does not exist
            pass
        except User.MultipleObjectsReturned:  # duplicate user
            logger.error("found duplicate mail addresses at MailLoginBackend.authenticate().\tmail:%s", username)
        else:
            if user.check_password(password):  # the password matches.
                return user

        return None

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        """
        overriding this method is obligated to be a backend.
        subclasses don't need to override this again.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SnsBackend(object):
    sns_name = None
    debug_data = None

    def __init__(self):
        self.kwargs = None

    def authenticate(self, **kwargs):
        """
        subclasses should check fields before proceeding to this procedure below.
        skip_registration parameter is used to reuse sns authenticate function without creating new user
        from users.views_api.Me api for connecting sns to existing user.
        :return User, None or int
        User instance if it already exists or is created with the returned SNS id,
        None if User.is_active=False,
        int if skip_registration option is True with no user associated with the SNS account
        """
        self.kwargs = kwargs
        data = self.request()
        if data:
            # validation
            # id
            if not data.get('id'):
                raise AE108()
            # verification
            queryset = self.get_queryset_for_existing_user(data)
            if queryset.exists():
                if queryset[0].is_active:
                    logger.info('returning user:%s using %s.', queryset[0].id, self.__class__.__name__)
                    return queryset[0]

                logger.warning('banned/disabled user:%s tried to login using %s.',
                               queryset[0].id, self.__class__.__name__)
                return None  # disabled user

            if kwargs.get('skip_registration', False):
                return data.get('id')

            new_user = self.register(data)  # new user
            logger.info('new user:%s using %s.', new_user.id, self.__class__.__name__)
            return new_user

    def request(self):
        """
        Subclasses should overwrite this to use other authorisation libraries such as oauth.
        :return dict or can be None
        """
        data = None
        try:
            # fetch using api
            data = requests.get(self.get_url()).json()
        except Exception as e:
            if hasattr(e, 'reason'):
                logger.error(e.reason)
            elif hasattr(e, 'code'):
                logger.error(e.code)
        return data

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        """
        overriding this method is obligated to be a backend.
        subclasses don't need to override this again.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_queryset_for_existing_user(self, data):
        """
        just return filtered queryset. subclasses don't need to filter enabled=True and such since authenticate() does
        it.
        """
        pass

    def get_url(self, **kwargs):
        """
        return api url.
        """
        pass

    def register(self, me):
        """
        called when the user is newbie.
        """
        # username validation.
        username = self.kwargs.get('username')
        from users.views_api import validate_user_data
        validate_user_data(username=username)


class FacebookBackend(SnsBackend):
    """
    required: facebook_token
    """
    sns_name = 'Facebook'

    def authenticate(self, **kwargs):
        if not kwargs.get('facebook_token'):
            return None
        return super(FacebookBackend, self).authenticate(**kwargs)

    def get_queryset_for_existing_user(self, data):
        return User.objects.filter(facebook_id=data.get('id'))

    def get_url(self):
        return '{}/me?access_token={}'.format(
            GRAPH_API_URL,
            self.kwargs.get('facebook_token')
        )

    def register(self, me):
        """
        adding fields below is not sufficient in case of additional DB field.
        also need to modify self.model() in create_user.
        """
        super(FacebookBackend, self).register(me)
        # email validation
        email = me.get('email')
        if email:
            try:
                validators.validate_email_leniently(email)
            except ValidationError:
                logger.warning('email, %s is not a valid email address.', email)
                # discard the address.
                email = None

        if email and User.objects.filter(email=email).exists():
            raise AE107()

        # noinspection PyProtectedMember
        user = User.objects.create_api_user(
            # get it from the parameters given to authenticate().
            username=self.kwargs.get('username'),
            nickname=self.kwargs.get('username'),
            # from the SNS.
            facebook_id=me.get('id'),
            profile=string.ellipsis(me.get('description'), User._meta.get_field('profile').max_length),
            profile_image_url="https://graph.facebook.com/{}/picture".format(me.get('id')),
            email=email,
        )
        return user


class TwitterBackend(SnsBackend):
    """
    required: twitter_access_token and twitter_access_token_secret
    """
    sns_name = 'Twitter'

    def authenticate(self, **kwargs):
        if not kwargs.get('twitter_access_token') or not kwargs.get('twitter_access_token_secret'):
            return None
        return super(TwitterBackend, self).authenticate(**kwargs)

    def request(self):
        session = OAuth1Session(consumer_key=getattr(settings, 'TWITTER_CONSUMER_KEY'),
                                consumer_secret=getattr(settings, 'TWITTER_CONSUMER_SECRET'),
                                access_token=self.kwargs.get('twitter_access_token'),
                                access_token_secret=self.kwargs.get('twitter_access_token_secret'))
        try:
            response = session.get(self.get_url())
            if response.status_code == 200:
                return response.json()
            else:
                # log error detail.
                logger.error(response.text)
        except RequestException as e:
            logger.error(str(e))

    def get_queryset_for_existing_user(self, data):
        return User.objects.filter(twitter_id=data.get('id'))

    def get_url(self):
        return '{}/account/verify_credentials.json'.format(TWITTER_API_URL)

    def register(self, me):
        """
        adding fields below is not sufficient in case of additional DB field.
        also need to modify self.model() in create_user.
        """
        super(TwitterBackend, self).register(me)
        # noinspection PyProtectedMember
        user = User.objects.create_api_user(
            # get it from the parameters given to authenticate().
            username=self.kwargs.get('username'),
            nickname=self.kwargs.get('username'),
            # from the SNS.
            twitter_id=me.get('id'),
            profile=string.ellipsis(me.get('description'), User._meta.get_field('profile').max_length),
            profile_image_url=me.get('profile_image_url_https').replace('_normal', '') if me.get('profile_image_url_https') else '',
        )
        return user


class InstagramBackend(SnsBackend):
    """
    required: instagram_token
    """
    sns_name = 'Instagram'

    def authenticate(self, **kwargs):
        if not kwargs.get('instagram_token'):
            return None
        return super(InstagramBackend, self).authenticate(**kwargs)

    def get_queryset_for_existing_user(self, data):
        queryset = User.objects.filter(instagram_id=data.get('id'))
        users = queryset.all()
        for user in users:
            if user.extra.get('instagram_username') is not None and user.extra.get(
                    'instagram_username', '') == data.get('username'):
                return queryset
            user.extra['instagram_username'] = data.get('username')
            user.save()
        queryset = User.objects.filter(instagram_id=data.get('id'))
        return queryset

    def get_url(self):
        return '{}/users/self/?access_token={}'.format(INSTAGRAM_API_URL, self.kwargs.get('instagram_token'))

    def request(self):
        data = super(InstagramBackend, self).request()

        if data and data.get('meta', {}).get('code', {}) == 200:
            data = data.get('data')

        return data

    def register(self, me):
        """
        adding fields below is not sufficient in case of additional DB field.
        also need to modify self.model() in create_user.
        """
        super(InstagramBackend, self).register(me)

        # set extra
        extra = {
            'instagram_username': me.get('username')
        }
        # noinspection PyProtectedMember
        user = User.objects.create_api_user(
            # get it from the parameters given to authenticate().
            username=self.kwargs.get('username'),
            nickname=self.kwargs.get('username'),
            # from the SNS.
            instagram_id=me.get('id'),
            profile=string.ellipsis(me.get('bio'), User._meta.get_field('profile').max_length),
            profile_image_url=me.get('profile_picture'),
            extra=extra
        )
        return user


class LineBackend(SnsBackend):
    """
    required: line_token
    """
    sns_name = 'Line'

    def authenticate(self, **kwargs):
        if not kwargs.get('line_token'):
            return None
        return super(LineBackend, self).authenticate(**kwargs)

    def get_queryset_for_existing_user(self, data):
        return User.objects.filter(line_id=data.get('id'))

    def get_url(self):
        return '{}/profile/?access_token={}'.format(LINE_API_URL, self.kwargs.get('line_token'))

    def request(self):
        try:
            response = requests.get(self.get_url(), headers={
                'Authorization': 'Bearer {}'.format(self.kwargs.get('line_token'))}
            )
            if response.status_code == 200:
                response_json = response.json()
                response_json['id'] = response_json.get('userId')
                return response_json
            else:
                # log error detail.
                logger.error(response.text)
        except RequestException as e:
            logger.error(str(e))

    def register(self, me):
        """
        adding fields below is not sufficient in case of additional DB field.
        also need to modify self.model() in create_user.
        """
        super(LineBackend, self).register(me)

        # noinspection PyProtectedMember
        user = User.objects.create_api_user(
            # get it from the parameters given to authenticate().
            username=self.kwargs.get('username'),
            nickname=self.kwargs.get('username'),
            # from the SNS.
            line_id=me.get('id'),
            profile=string.ellipsis(me.get('statusMessage'), User._meta.get_field('profile').max_length),
            profile_image_url=me.get('pictureUrl')
        )
        return user
