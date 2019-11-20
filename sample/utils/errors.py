class MimeTypeError(Exception):
    """Raised when the mime type is not allowed"""
    def __init__(self, message=None):
        if message:
            self.message = "Not allowed mime type: {0}".format(message)
        else:
            self.message = "Not allowed mime type"

        super(MimeTypeError, self).__init__(self.message)


class ImageSizeOverError(Exception):
    """Raised when the size of image is more than the size you defined(file_size = byte)"""
    def __init__(self, file_size=None):
        if file_size:
            max_mbyte = int(file_size / 1024**2)
            self.message = "Size of the image is over %d MB" % max_mbyte
        else:
            self.message = "Size of the image is over"

        super(ImageSizeOverError, self).__init__(self.message)


class GetError(Exception):
    """Raised when the gets are not enough"""
    def __init__(self, message=None):
        if message:
            self.message = "Not enough gets: {0}".format(message)
        else:
            self.message = "Not enough gets"

        super(GetError, self).__init__(self.message)


class PostError(Exception):
    """Raised when the posts are not enough"""
    def __init__(self, message=None):
        if message:
            self.message = "Not enough posts: {0}".format(message)
        else:
            self.message = "Not enough posts"

        super(PostError, self).__init__(self.message)


class ScraperError(Exception):
    """Raised when scraper fails at any defined action"""


class AbandonAction(Exception):
    """Raised when current action should be finished"""


class TooManyRequests(OSError):
    """Raised when server returned too many request exception"""
