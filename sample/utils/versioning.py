from django.conf import settings
from rest_framework.versioning import AcceptHeaderVersioning


class NumericAcceptHeaderVersioning(AcceptHeaderVersioning):
    """
    Convert version string to float.
    """

    def determine_version(self, request, *args, **kwargs):
        return float(super(NumericAcceptHeaderVersioning, self).determine_version(request, *args, **kwargs))


def get_version(request):
    """ an error "'HttpRequest' object has no attribute 'version'" occurs thanks to django-rest-swagger
    if you use request.version in get_serializer_class() in view. this function workaround the issue
    by safely returning the default version number.
    :param request: request object
    :return: float version number
    """
    return getattr(request, 'version', float(settings.REST_FRAMEWORK['DEFAULT_VERSION']))