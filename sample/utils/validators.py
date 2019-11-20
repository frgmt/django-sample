import logging
from datetime import datetime
from uuid import UUID

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


def validate_file_content_type(file, allowed_types):
    """
    Verifies file's content type.
    :param file: file to be verified
    :param allowed_types: iterable containing allowed types as strings
    :raise: ValidationError if file's type is not in provided iterable
    """
    if file.content_type not in allowed_types:
        raise ValidationError(_('validation_mime_type_is_not_allowed'))


def validate_file_max_size(file, max_size):
    """
    Verifies if file's size doesn't exceed provided maximum value.
    :param file: file to be verified
    :param max_size: maximum allowed size in bytes
    :raise: ValidationError if file's size is bigger than provided value
    """
    if file._size > max_size:
        raise ValidationError(_('validation_image_file_size_is_too_large'))


def validate_date_format(date_str, date_format="%Y-%m-%d"):
    """
    Verifies if date string is in correct format.
    :param date_str: string to validate
    :param date_format: format against which date should be validated
    :return: True if date string is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        return False
    return True


def validate_convertible_to_int(string):
    try:
        int(string)
    except ValueError:
        return False
    return True


def uuid_valid(string, version=4):
    try:
        UUID(string, version=version)
    except ValueError:
        return False
    return True


def validate_sequence_values_convertible_to_int(sequence):
    for value in sequence:
        if not validate_convertible_to_int(value):
            return False
    return True
