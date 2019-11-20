# coding=utf-8
import codecs
import csv
import re
import unicodedata

import six
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.datetime_safe import new_datetime, datetime
from django.utils.encoding import smart_text


# From Python2 csv module docs
# https://docs.python.org/2/library/csv.html
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [smart_text(s, "utf-8") for s in row]

    def __iter__(self):
        return self


def ellipsis(text, max_length):
    if text:
        limit = max_length - 1
        return text[:limit] + (text[limit:] and u'…')


def parse_lazy_datetime(string):
    value = None
    try:
        value = parse_date(string)
        if value is None:
            value = parse_datetime(string)
        else:
            value = new_datetime(value)
    except ValueError:
        pass
    if value:
        return value
    # fall back to string.
    return string


def validate_datetime_format(string):
    if isinstance(parse_lazy_datetime(string), datetime):
        return True
    return False


def join_numeric(numeric_list, delimiter=''):
    return delimiter.join(str(n) for n in numeric_list)


def is_url(string):
    """
    Checks string if its format is URL but doesn't access the URL to make sure it's valid and alive.
    :param string: string to be checked
    :return: True if the string format is URL.
    """
    return re.match(r'https?://', string, re.IGNORECASE) is not None


def strip_cp932_incompatible_characters(string):
    """
    Strip problematic characters from the text for csv output.
    :param string: string to be processed.
    :return: str (not bytes)
    """
    if string and isinstance(string, six.text_type):
        return string.encode(encoding='cp932', errors='ignore').decode(encoding='cp932')
    return ''


def remove_control_characters(string):
    """
        Strip control characters from the text.
        :param string: string to be processed.
        :return: str (not bytes)
        """
    return ''.join(character for character in string if unicodedata.category(character)[0] != 'C')


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               "\U0001F600-\U0001F64F"  # emoticons
                               "\U0001F300-\U0001F5FF"  # symbols & pictographs
                               "\U0001F680-\U0001F6FF"  # transport & map symbols
                               "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
