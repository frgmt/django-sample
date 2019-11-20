
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler

from utils.errors_api import ApiBaseError


def custom_exception_handler(exc, context):
    """ inject code attribute to the response.
    :param exc: any Exception class
    :param context: view context(view, args, kwargs, request)
    :return: response
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        # catching serializers.ValidationError({'code': 999, 'detail': 'error message'}) raised in API.
        # the dict argument is saved as exc.detail and each record is converted to list,
        # so we need to convert the attributes into a valid response structure.
        if isinstance(exc, serializers.ValidationError) and isinstance(exc.detail, dict):
            code = exc.detail.get('code')
            # unpack list of code.
            if isinstance(code, list) and len(code) > 0:
                code = code[0]
            try:
                # extract code value and convert it into int.
                response.data['code'] = int(code)
            except (ValueError, TypeError):
                # ignore conversion error.
                pass
            detail = exc.detail.get('detail')
            # unpack list of detail.
            if isinstance(detail, list) and len(detail) > 0:
                detail = detail[0]
            response.data['detail'] = detail

        # catching sub-classes of ApiBaseError
        elif isinstance(exc, ApiBaseError):
            response.data['code'] = exc.code
            response.data['detail'] = exc.detail

        # catching other generic error
        else:
            try:
                code = int(getattr(exc, 'code', None))
                response.data['code'] = code
                if code and not hasattr(exc, 'status_code'):
                    response.data['status_code'] = HTTP_400_BAD_REQUEST
            except (ValueError, TypeError):
                # ignore conversion error.
                pass

    return response


def build_api_error(exc_class, error):
    """ NOT IN USE at the moment.
    :param exc_class: Exception class
    :param error: instance of ApiBaseError's sub-classes.
    :return: raise-ready Exception object.
    """
    assert issubclass(error, ApiBaseError)
    exception = exc_class(error.detail)
    exception.code = error.code
    return exception
