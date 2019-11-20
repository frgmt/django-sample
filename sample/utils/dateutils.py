# coding=utf-8
from __future__ import absolute_import

import datetime

from django.utils import timezone


def get_utc_time(dt=None, delta=None):
    """
    :param dt: jst time.
    :param delta: timedelta.
    :return: utc time.
    """
    if dt is None:
        dt = timezone.now() + timezone.timedelta(hours=9)
    if delta is not None:
        dt += delta
    return dt - timezone.timedelta(hours=9)


def get_jst_time(dt=None, delta=None):
    """
    :param dt: utc time.
    :param delta: timedelta.
    :return: jst time.
    """
    if dt is None:
        dt = timezone.now()
    if delta is not None:
        dt += delta
    return dt + timezone.timedelta(hours=9)


def combine_min_time(date):
    """
    :param date: datetime to base on.
    :return: timezone aware datetime combined with time.min.
    """
    return timezone.make_aware(datetime.datetime.combine(date, datetime.time.min))


def combine_max_time(date):
    """
    :param date: datetime to base on.
    :return: timezone aware datetime combined with time.max.
    """
    return timezone.make_aware(datetime.datetime.combine(date, datetime.time.max))


def sec_to_time(seconds):
    """
    Converts seconds to time string. ex.: 36000 -> '10:00:00'
    :param seconds: <int> seconds to convert
    :return: <str> time as string
    """
    return str(timezone.timedelta(seconds=seconds))


def time_to_sec(time_obj):
    """
    Converts datetime.time to seconds.
    :param time_obj: datetime.time object
    :return: <int> time in seconds
    """
    seconds = datetime.timedelta(hours=time_obj.hour, minutes=time_obj.minute).total_seconds()
    return int(seconds)


def date_range(start_date, end_date):
    """
    Date range for db.
    :param start_date: datetime object
    :param end_date: datetime object
    :return: min and max date tuple
    """
    return (
        combine_min_time(start_date) - timezone.timedelta(hours=9),
        combine_max_time(end_date) - timezone.timedelta(hours=9)
    )
