from functools import wraps
from django.http import HttpResponseForbidden


def superuser_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                "You do not have permission to access this page."
            )

    return wrap
