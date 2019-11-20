import requests
from bs4 import BeautifulSoup


class WebExtraction(object):
    def __init__(self, url):
        self.url = url
        self._context = ""
        self._meta = {}
        self._soup = None
        self._get_context()

    def _get_context(self):
        try:
            content = requests.get(self.url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'},
                                   allow_redirects=True,
                                   timeout=7).content
        except Exception as e:
            raise e
        else:
            self._soup = BeautifulSoup(content, 'html.parser')
            self._meta = {meta.get("name") if meta.get("name") else meta.get("property"): meta.get("content")
                          for meta in self._soup.find_all("meta")}

    def get_title(self):
        try:
            title = self._soup.title.string
        except AttributeError:
            title = ""
        return title

    def get_meta(self):
        return self._meta

    def get_og_img(self):
        return self._meta.get("og:image", "")

    def get_description(self):
        if self._meta.get("description"):
            return self._meta.get("description")
        else:
            return self._meta.get("og:description", "")
