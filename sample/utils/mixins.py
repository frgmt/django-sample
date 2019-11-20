# -*- coding:utf-8 -*-

import logging

from django.conf import settings
from django.http import QueryDict

from sample.paginations import StandardCursorPagination

logger = logging.getLogger('{0}.{1}'.format(getattr(settings, 'LOG_ROOT'), __name__))


class PaginationSelectorMixin(object):
    """
    Use with ListAPIView or ListModelMixin to change paginator from the default to CursorPagination
    when version >= 1 and page_size or page parameter is not given.
    Note1: page_size parameter is used only by PageNumberPagination class.
    Note2: User classes must call super().get() instead of calling self.list().
    """

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit
    def get(self, request, *args, **kwargs):
        if (request.version >= 1 and
                    request.query_params.get('page_size') is None and
                    request.query_params.get('page') is None and
            # ordering parameter is mandatory for CursorPagination.
                    getattr(self, 'ordering', None) is not None and
            # the paginator doesn't work with relational ordering.
                    '__' not in ''.join(getattr(self, 'ordering'))):
            self._paginator = StandardCursorPagination()

        # try to call parent's get().
        # suppress error, "AttributeError: 'super' object has no attribute 'get'".
        if hasattr(super(PaginationSelectorMixin, self), 'get'):
            return super(PaginationSelectorMixin, self).get(request, *args, **kwargs)
        # call self.list() directly if the super class doesn't have get().
        if hasattr(self, 'list'):
            return self.list(request, *args, **kwargs)
        # or call super().list() instead.
        return super(PaginationSelectorMixin, self).list(request, *args, **kwargs)


class ImageManagerMixin(object):
    def get_image_thumb_url(self):
        if self.image_url:
            return self.image_url.replace('_l', '_thumb')
        else:
            return self.image_url

    def get_image_small_url(self):
        if self.image_url:
            return self.image_url.replace('_l', '_s')
        else:
            return self.image_url

    def get_image_medium_url(self):
        if self.image_url:
            return self.image_url.replace('_l', '_m')
        else:
            return self.image_url

    def get_image_url(self):
        return self.image_url


class OverwriteRequestDataMixin(object):
    """ Allows views to add extra data to the request.data by implementing overwrite_data().
    """

    def overwrite_data(self, data):
        pass

    def get_serializer(self, *args, **kwargs):
        # finding data in kwargs suggests that we're creating or updating the object.
        if kwargs.get('data') is not None:
            data = kwargs['data']
            # force QueryDict as mutable.
            if isinstance(data, QueryDict):
                data._mutable = True
            # add the extra data.
            self.overwrite_data(data)
            # and restore QueryDict if applicable.
            if isinstance(data, QueryDict):
                # force QueryDict as mutable.
                data._mutable = False
        # noinspection PyUnresolvedReferences
        return super(OverwriteRequestDataMixin, self).get_serializer(*args, **kwargs)
