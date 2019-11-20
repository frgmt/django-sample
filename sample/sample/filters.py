from django.utils import six
from django_filters import compat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class CustomDjangoFilterBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        # Most of the implementation is copied from DjangoFilterBackend.
        # Main purpose is to populate description from FilterSet's Meta attribute rather than useless form's help_text.

        # This is not compatible with widgets where the query param differs from the
        # filter's attribute name. Notably, this includes `MultiWidget`, where query
        # params will be of the format `<name>_0`, `<name>_1`, etc...
        assert compat.coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        filter_class = self.get_filter_class(view, view.get_queryset())
        description_dict = getattr(filter_class.Meta, 'descriptions', {}) if filter_class is not None else {}

        return [] if not filter_class else [
            compat.coreapi.Field(
                name=field_name, required=False, location='query',
                description=description_dict.get(field_name, six.text_type(field.field.help_text)))
            for field_name, field in filter_class().filters.items()]


class CustomOrderingFilter(OrderingFilter):
    def get_schema_fields(self, view):
        description = ''
        if hasattr(view, 'ordering_fields') and view.ordering_fields:
            description = '`{}` can be used as value.'.format(view.ordering_fields)
            if hasattr(view, 'ordering') and view.ordering:
                description += ' Default ordering is `{}`'.format(view.ordering)
        return [
            compat.coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                description=description
            )
        ]
