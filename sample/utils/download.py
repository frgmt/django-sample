import os
import socket
import uuid

import requests
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.six import moves

from utils.errors import MimeTypeError, ImageSizeOverError

DEFAULT_MAX_DOWNLOAD_FILE_SIZE = 10485760  # 10MB


class DownloadImage(object):
    download_max_file_size = DEFAULT_MAX_DOWNLOAD_FILE_SIZE
    allow_image_mime_type = settings.ALLOW_IMAGE_MIME_TYPE

    def __init__(self, url):
        self.url = url.strip()
        self.mimetype = ""
        self.name = ""
        self.size = 0
        self._data = None

        self._get_image()

    def _get_image(self):
        try:
            if self._is_proxy():
                response = requests.get(self.url, timeout=5, proxies=settings.PROXIES, headers={'User-Agent': 'Mozilla/5.0'})
            else:
                response = requests.get(self.url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})

            headers = response.headers
            self.mimetype = headers.get('content-type')
            if headers.get('content-length'):
                self.size = int(headers.get('content-length'))

                if self.size > self.download_max_file_size:
                    raise ImageSizeOverError(self.download_max_file_size)

            # if image is from amana or pashadelic, through this check
            if self.mimetype not in self.allow_image_mime_type and not self._is_proxy() and not self._is_pashadelic():
                raise MimeTypeError(self.mimetype)

            self._data = response.content
            response.connection.close()
            response.connection = None
            response = None

        except (moves.urllib.error.URLError, socket.timeout, MimeTypeError, ImageSizeOverError, ValueError) as e:
            raise e

    def write(self):
        self.name = uuid.uuid4().hex
        img_tmp = TemporaryUploadedFile(self.name, self.mimetype, self.size, None)
        img_tmp.write(self._data)
        img_tmp.flush()

        # use temporary file size if there is no content-length in response header
        # The file size is validated at converter
        if self.size == 0:
            img_tmp.size = os.path.getsize(img_tmp.temporary_file_path())

        self._data = None
        return img_tmp

    # if the image is from pashadelic, return True
    def _is_pashadelic(self):
        return 'storage.googleapis.com/1d9d6837-13ca-49ce-868f-5a898d50a328/' in self.url

    # if needs proxy, return True
    def _is_proxy(self):
        return 'amanaimages' in self.url
