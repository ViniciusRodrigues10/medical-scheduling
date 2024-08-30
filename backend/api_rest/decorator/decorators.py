from functools import wraps
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework import status


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(request.user.is_superuser)
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return Response(
            {
                "detail": "Permission denied. You must be a superuser to perform this action."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    return _wrapped_view


def login_required_custom(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Você não está logado")

    return wrap


def log_request(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(f"Entering {func.__name__}")
            response = func(*args, **kwargs)
            logger.log(f"Exiting {func.__name__}")
            return response

        return wrapper

    return decorator
