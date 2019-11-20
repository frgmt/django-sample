import re

from django.core.validators import EmailValidator


class LenientEmailValidator(EmailValidator):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+[-!#$%&'*+/=?^_`{}\.|~0-9A-Z]*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',  # quoted-string
        re.IGNORECASE)


validate_email_leniently = LenientEmailValidator()
