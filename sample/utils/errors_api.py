import re

from django.utils.translation import ugettext_lazy as _
from rest_framework import status, serializers
from rest_framework.exceptions import APIException


class ApiBaseError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = None
    code = None

    code_pattern = re.compile(r'([0-9]+)$')

    def __init__(self, detail=None, **kwargs):
        if self.code is None:
            # set the code attribute automatically from class name of subclass.
            match = self.code_pattern.search(self.__class__.__name__)
            if match:
                self.code = int(match.group(1))
        assert self.default_detail and self.code

        # interpolation
        if kwargs:
            detail = self.default_detail % kwargs
        super(ApiBaseError, self).__init__(detail)

    def get_serializer_validation_error(self):
        """ used to raise error in serializer.validate()
        :return: raise-ready serializers.ValidationError
        """
        return serializers.ValidationError({'code': self.code, 'detail': self.detail})

