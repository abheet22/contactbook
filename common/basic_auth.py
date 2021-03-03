from functools import wraps
from .basicauth_utils import validate_request
from django.conf import settings
from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self, request):
        super(HttpResponseUnauthorized, self).__init__("""Request is not authorized.""")
        realm = getattr(settings, "BASICAUTH_REALM", "Secure resource")
        self["WWW-Authenticate"] = 'Basic realm="{}"'.format(realm)


def basic_auth_required(func=None, target_test=(lambda request: True)):
    def actual_decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if target_test(request) and not validate_request(request):
                return HttpResponseUnauthorized(request)
            return view_func(request, *args, **kwargs)

        return _wrapped

    if func:
        return actual_decorator(func)
    else:
        return actual_decorator
