# -*- coding:utf-8 -*-

"""
utils
"""
import logging

import requests
from articles.constants import ARTICLE_CONTENT_TYPE
from articles.dynamodb_models import DyPaidImageUsageByUser
from articles.permissions import CanEditArticleDynamic
from django.conf import settings
from django.utils.six import moves
from rest_framework import status
from rest_framework import views
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import HasPermissionChangeArticle
from utils.images.converters import (
    ImageProcessorForArticle,
    CroppedImageProcessorForArticle,
    MovieProcessorForArticle
)
from utils.permissions import UrlImagePermission

from utils.download import DownloadImage
from utils.errors_api import AE501, AE502, AE503, AE504, AE505, AE401
from utils.mixins import ValidationMixin
from utils.webextraction import WebExtraction

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


class UrlValidator(views.APIView):
    """
    Check if url is valid by checking head request response

    # Parameters

    - url: Image reference url to check
    """
    permission_classes = (IsAuthenticated, HasPermissionChangeArticle)
    throttle_scope = 'edit'

    def get(self, request, *args, **kwargs):
        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('id'))

        data = {}
        response_status = None

        try:
            url = request.GET.get('url')
            if not url:
                raise AE504()
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
            }, allow_redirects=True, timeout=7)
            response_status = response.status_code
            if response.ok:
                data["status"] = response.status_code
                data["detail"] = response.reason
            else:
                raise AE504()
        except requests.RequestException:
            data["status"] = AE504().code
            data["detail"] = AE504().detail
        except AE504 as e:
            data["status"] = e.code
            data["detail"] = e.default_detail

        return Response(data=data, status=response_status if response_status else status.HTTP_400_BAD_REQUEST)


class SiteInfo(views.APIView):
    """
    外部のWEBページのMETA情報を取得するAPI（記事編集の LINK コンテンツで利用）

    # Parameters

    - url: META情報を取得したい対象のURL
    - id: LINKコンテンツを挿入する対象記事
    - is_upload: 任意。og:image をアップロードしたければ true
    """
    permission_classes = (IsAuthenticated, CanEditArticleDynamic)
    throttle_scope = 'edit'

    def post(self, request, *args, **kwargs):
        if not (request.data.get('url') and request.data.get('id')):
            raise AE501()
        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('id'))
        # logging
        logger.info('{klass} is used by {user} and the data is {data}.'.format(
            klass=type(self).__name__, user=request.user.username, data=request.data))
        try:
            site = WebExtraction(request.data.get("url"))
        except Exception as e:
            raise AE504(e)
        if site.get_og_img():
            if request.data.get("is_upload"):
                try:
                    tmpfile = DownloadImage(site.get_og_img()).write()
                    im = self.image_process(tmpfile, request.data.get("id"))
                    im.resize()
                    image_url = im.save()
                except Exception:
                    image_url = ""
            else:
                image_url = site.get_og_img()
        else:
            image_url = ""

        return Response({
            "url": site.url,
            "title": site.get_title(),
            "description": site.get_description(),
            "image": image_url
        }, status=status.HTTP_201_CREATED)

    def image_process(self, tmpfile, request_id):
        return ImageProcessorForArticle(tmpfile, request_id)


class UrlImage(ValidationMixin, views.APIView):
    permission_classes = (IsAuthenticated, CanEditArticleDynamic, UrlImagePermission)
    throttle_scope = 'edit'

    def post(self, request, format=None):
        if not (request.data.get('url') and request.data.get('id')):
            raise AE501()
        else:
            if (request.data.get('url')
                and request.data.get('content_type') == ARTICLE_CONTENT_TYPE['IMAGE']['TYPE']
                and request.data.get('sub_content_type') in (
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['URL'],
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['LOCAL'],
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['BING']
                )):
                if not self.is_safe_url(request.data.get('url')):
                    raise AE503()

        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('id'))
        # logging
        logger.info('{klass} is used by {user} and the data is {data}.'.format(
            klass=type(self).__name__, user=request.user.username, data=request.data))
        try:
            tmpfile = DownloadImage(self._get_url()).write()

            # if image is from amana or pashadelic (through google storage), attach content type
            if 'amanaimages' in request.data.get('url'):
                tmpfile.content_type = 'image/jpeg'
            if 'storage.googleapis.com/1d9d6837-13ca-49ce-868f-5a898d50a328/' in request.data.get('url'):
                tmpfile.content_type = 'image/jpeg'

            is_public = True
            if request.data.get('content_type') == ARTICLE_CONTENT_TYPE['IMAGE']['TYPE']:
                if request.data.get('sub_content_type') in (
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['INSTAGRAM'],
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['PINTEREST'],
                        ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['OZMALL'],
                ):
                    is_public = False

            im = self.image_process(tmpfile, request.data.get("id"))
            im.resize()
            image_url = im.save(is_public=is_public)

            # if the image is from Amana or Pixta create/update the count entry for the username in dynamodb
            if request.data.get('sub_content_type') in (
                    ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['PIXTA'],
                    ARTICLE_CONTENT_TYPE['IMAGE']['SUB_CONTENT_TYPE']['AMANA'],
            ):
                DyPaidImageUsageByUser().update_count(request.user.username)
            return Response(
                {
                    "image": image_url,
                    "image_reference_url": request.data.get('url'),
                    "image_register_user": request.user.id
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            raise AE505(e)

    def _get_url(self):
        """ The frontend base controller, UploadFromAPIControllerBase is tightly coupled with UrlImage service class
        so the code can get messy if you try to define a separate view for Pixta. That's why these codes are hooked
        into this view.
        :return: string url
        """
        # PIXTA
        if UrlImagePermission.is_pixta_request(self.request):
            # extract photo_id from URL.
            try:
                parsed_url = moves.urllib_parse.urlparse(self.request.data.get('url'))
                path = parsed_url[2]
                segments = path.split(u'/')
                img_name = segments[5].split(u'.')
                photo_id = img_name[0]
            except Exception:
                raise AE501()

            url = '{}/images/download/{}?size=m&format=jpg'.format(settings.PIXTA_BASE_URL, photo_id)
            headers = {'Authorization': 'Bearer %s' % settings.PIXTA_TOKEN}
            try:
                r = requests.get(url, headers=headers, allow_redirects=False)
                # Location header contains the real URL to the image.
                return r.headers['location']
            except Exception:
                raise AE401()
        # AMANA
        elif UrlImagePermission.is_amana_request(self.request):
            return ''.join([self.request.data.get('link_url'), 'M'])

        return self.request.data.get('url')

    def image_process(self, tmpfile, request_id):
        return ImageProcessorForArticle(tmpfile, request_id)


class UploadImage(views.APIView):
    """ This class is used with article and corporate.
    """
    permission_classes = (IsAuthenticated, CanEditArticleDynamic)
    parser_classes = (MultiPartParser, FormParser)
    throttle_scope = 'edit'

    def post(self, request, format=None):
        if not (request.data.get('file') and request.data.get('id')):
            raise AE502()
        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('id'))
        # logging
        logger.info('{klass} is used by {user} and the data is {data}.'.format(
            klass=type(self).__name__, user=request.user.username, data=request.data))
        image_reference_url = request.data.get('image_reference_url', "")
        image_register_user = request.user.id
        try:
            im = self.image_process(request.data.get('file'), request.data.get('id'))
            im.resize()
            image_url = im.save()
            return Response(
                {
                    "image": image_url,
                    "image_reference_url": image_reference_url,
                    "image_register_user": image_register_user
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            raise AE505(e)

    def image_process(self, tmpfile, request_id):
        return ImageProcessorForArticle(tmpfile, request_id)


class UploadMovie(views.APIView):
    """ This class is used with article.
    """
    permission_classes = (IsAuthenticated, CanEditArticleDynamic)
    parser_classes = (MultiPartParser, FormParser)
    throttle_scope = 'edit'

    def post(self, request, format=None):
        if not (request.data.get('file_name') and request.data.get('file_type') and request.data.get('id')):
            raise AE502()
        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('id'))
        # logging
        logger.info('{klass} is used by {user} and the data is {data}.'.format(
            klass=type(self).__name__, user=request.user.username, data=request.data))
        try:
            movie = self.movie_process(
                request.data.get('file_name'),
                request.data.get('file_type'),
                request.data.get('id')
            )
            data = movie.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            raise AE505(e)

    def movie_process(self, file_name, file_type, request_id):
        return MovieProcessorForArticle(file_name, file_type, request_id)


class UploadCropImage(views.APIView):
    permission_classes = (IsAuthenticated, CanEditArticleDynamic)
    parser_classes = (MultiPartParser, FormParser)
    throttle_scope = 'edit'

    def put(self, request, format=None):
        if not (request.data.get('file') and request.data.get('article_id')):
            raise AE502()
        # manual permission check.
        self.check_object_permissions(self.request, request.data.get('article_id'))
        # logging
        logger.info('{klass} is used by {user} and the data is {data}.'.format(
            klass=type(self).__name__, user=request.user.username, data=request.data))
        try:
            # crop image
            im = self.image_process(
                request.data.get('file'),
                request.data.get('image_url').split('/')[-1],
                request.data.get('article_id'),
                request.data.get('is_main') == 'true'
            )
            im.resize(quality=85)
            image_url = im.save()
        except Exception as e:
            raise AE505(e)
        else:
            return Response({"image": image_url}, status=status.HTTP_201_CREATED)

    def image_process(self, tmpfile, filename, request_id, is_main):
        return CroppedImageProcessorForArticle(tmpfile, filename, request_id, is_main)
