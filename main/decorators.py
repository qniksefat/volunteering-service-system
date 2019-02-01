from functools import wraps

from django.core.exceptions import PermissionDenied

from main.models import User


def charity_required(func=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == User.CHARITY:
                request.charity = request.user.charity
                return view_func(request, *args, **kwargs)
            raise PermissionDenied()

        return _wrapped_view

    if func:
        return decorator(func)
    return decorator
