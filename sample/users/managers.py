# -*- coding:utf-8 -*-
import copy

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

from utils.errors_api import AE103, AE104


class UserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        """
        used on the web.
        """
        username = extra_fields.get('username')
        email = extra_fields.get('email')
        password = make_password(extra_fields.get('password'))
        facebook_id = self._convert_int_or_none(extra_fields.get('facebook_id'))
        twitter_id = self._convert_int_or_none(extra_fields.get('twitter_id'))
        instagram_id = self._convert_int_or_none(extra_fields.get('instagram_id'))
        line_id = extra_fields.get('line_id', None)
        if not username:
            is_active = True
            if facebook_id:
                username = 'FB%d' % facebook_id
            elif twitter_id:
                username = 'TW%d' % twitter_id
            elif instagram_id:
                username = 'IN%d' % instagram_id
            elif line_id:
                username = 'LI%s' % line_id
            else:
                raise ValueError('one of username, facebook_id, instagram_id, line_id and twitter_id is required.')
        else:
            is_active = False
            if not password:
                raise ValueError('password is required when username is present.')

        # check duplication
        if self.get_queryset().filter(email=email, is_active=False).exists():
            user = self.get_queryset().filter(email=email, is_active=False).get()
            user.username = username
            user.nickname = username
            user.facebook_id = facebook_id
            user.twitter_id = twitter_id
            user.instagram_id = instagram_id
            user.line_id = line_id
            user.password = password
        else:
            user = self.model(
                username=username,
                nickname=username,
                facebook_id=facebook_id,
                twitter_id=twitter_id,
                instagram_id=instagram_id,
                line_id=line_id,
                email=email,
                password=password,
                is_active=is_active
            )
        user.save(using=self._db)
        return user

    def create_api_user(self, **extra_fields):
        """
        used in the api.
        """
        fields = copy.copy(extra_fields)
        # pop fields
        username = fields.pop('username', None)
        email = BaseUserManager.normalize_email(fields.pop('email', None))
        password = make_password(fields.pop('password', None))
        facebook_id = self._convert_int_or_none(fields.pop('facebook_id', None))
        twitter_id = self._convert_int_or_none(fields.pop('twitter_id', None))
        instagram_id = self._convert_int_or_none(fields.pop('instagram_id', None))
        line_id = fields.pop('line_id', None)
        nickname = fields.pop('nickname', None)
        extra = fields.pop('extra', {'instagram_username': ''})
        activity_settings = fields.pop('activity_settings', {'comments_public': True})
        # validations
        if not username:
            raise AE104()
        if not any([facebook_id, twitter_id, instagram_id, line_id]) and not password:
            raise AE103()
        # remove None values from the fields to prevent error.
        for k, v in list(fields.items()):
            if v is None:
                del fields[k]

        user = self.model(
            username=username,
            nickname=nickname or username,
            facebook_id=facebook_id,
            twitter_id=twitter_id,
            instagram_id=instagram_id,
            line_id=line_id,
            email=email,
            password=password,
            is_active=True,
            extra=extra,
            activity_settings=activity_settings,
            **fields
        )
        user.full_clean()
        user.save(using=self._db)
        # set temporal flag to let view know that the user is just created and return 201 response.
        user.is_new = True
        return user

    # noinspection PyUnusedLocal
    def create_superuser(self, username, email, password, **extra_fields):
        user = self.model(
            username=username,
            nickname=username,
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.save(using=self._db)
        return user

    @staticmethod
    def _convert_int_or_none(source):
        if source is not None:
            return int(source)
        return None
