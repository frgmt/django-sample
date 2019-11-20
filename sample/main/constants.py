from enum import IntEnum


class ExternalLinkCategory(IntEnum):
    article_content = 1
    related_link = 2
    related_article = 3
    spot_content = 4


class CloudSearchContentType(IntEnum):
    location = 1
    tag = 2
    spot = 3
    article = 4
    spot_category_mapping = 5
    spot_scene = 6


DEVICE_UNKNOWN = 0
DEVICE_PC = 1
DEVICE_SP = 2
DEVICE_IOS = 3
DEVICE_ANDROID = 4

DEVICE_CHOICES = (
    (DEVICE_UNKNOWN, 'UNKNOWN'),
    (DEVICE_PC, 'PC'),
    (DEVICE_SP, 'SP'),
    (DEVICE_IOS, 'iOS'),
    (DEVICE_ANDROID, 'Android'),
)

PARTNER_CODE_sample = 101
PARTNER_CODE_sample_BLOG = 102
PARTNER_CODE_sample_BOOKS = 111
PARTNER_CODE_SMARTNEWS = 201
PARTNER_CODE_FACEBOOK = 301
PARTNER_CODE_TWITTER = 302
PARTNER_CODE_INSTAGRAM = 303
PARTNER_CODE_LINE = 304

PARTNER_CODE_CHOICES = (
    (PARTNER_CODE_sample, 'sample'),
    (PARTNER_CODE_sample_BLOG, 'sample_blog'),
    (PARTNER_CODE_sample_BOOKS, 'sample_books'),
    (PARTNER_CODE_SMARTNEWS, 'smartnews'),
    (PARTNER_CODE_FACEBOOK, 'facebook'),
    (PARTNER_CODE_TWITTER, 'twitter'),
    (PARTNER_CODE_INSTAGRAM, 'instagram'),
    (PARTNER_CODE_LINE, 'line'),
)
