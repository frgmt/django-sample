
import json

from django import forms
from django.utils import six


class JSONWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ""

        if not isinstance(value, six.string_types):
            value = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)

        return super(JSONWidget, self).render(name, value, attrs)
