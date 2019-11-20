# -*- coding:utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users import validators

MINIMUM_USERNAME_LENGTH = 3
MINIMUM_PASSWORD_LENGTH = 8


class LenientEmailField(models.EmailField):
    default_validators = [validators.validate_email_leniently]


class User(AbstractUser):
    # Default validator became UnicodeUsernameValidator under python3.
    username_validator = ASCIIUsernameValidator()
    # Re-declaration of username because of this issue, http://stackoverflow.com/a/41634646
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        # this usage of index_together is to merely add simple index to date_joined field declared in AbstractUser.
        # the result is completely the same as db_index.
        index_together = [['date_joined']]

    def __str__(self):
        return '%s' % (self.username,)
