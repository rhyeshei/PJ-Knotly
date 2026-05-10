from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.knotly.permissions import is_knotly_admin


def knotly_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_knotly_admin(request.user):
            return HttpResponseForbidden('You do not have permission to access Knotly dashboard.')
        return view_func(request, *args, **kwargs)

    return login_required(_wrapped_view)
