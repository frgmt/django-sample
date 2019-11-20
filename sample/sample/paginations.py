from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardCursorPagination(CursorPagination):
    page_size = 20


class FavoriteListItemPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = '{}_page'

    def __init__(self, page_type):
        self.page_query_param = self.page_query_param.format(page_type)
