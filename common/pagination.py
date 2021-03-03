import six
from urllib.parse import urlparse, urlencode, parse_qs
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from common import api_exceptions
from django.conf import settings
from collections import OrderedDict


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        ret = min(ret, cutoff)
    return ret


def replace_query_param(url, key, value):
    url_parts = list(urlparse(url))
    query = dict(parse_qs(url_parts[4]))
    query.update({key: value})
    url_parts[4] = urlencode(query, doseq=True)
    return url_parts[2] + "?" + url_parts[4]


class PageNumberPagination(object):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:
    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """

    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    # page_size = api_settings.PAGE_SIZE
    page_size = settings.API_PAGE_SIZE

    django_paginator_class = Paginator

    # Client can control the page using this query parameter.
    page_query_param = "page"

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'page_size'

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = None

    last_page_strings = ("last",)

    request = None

    paginator = None

    invalid_page_message = 'Invalid page "{page_number}": {message}.'

    def paginate_queryset(self, queryset, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(view)
        if not page_size:
            return None

        self.paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.request.GET.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = self.paginator.num_pages

        try:
            self.page = self.paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(page_number=page_number, message=six.text_type(exc))
            raise api_exceptions.NotFound(msg)

        return list(self.page)

    def get_paginated_response(self, data):
        meta = dict(
            [
                ("base", getattr(settings, "REQUEST_SCHEME") + "://" + self.request.get_host()),
                ("next", self.get_next_link()),
                ("count", self.paginator.count),
            ]
        )
        return OrderedDict([("data", data), ("meta", meta)])

    def get_page_size(self, view):
        if self.page_size_query_param:
            if getattr(view, 'max_page_size', None):
                self.max_page_size = view.max_page_size
            try:
                return _positive_int(
                    self.request.GET[self.page_size_query_param], strict=True, cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return replace_query_param(url, self.page_query_param, page_number)
