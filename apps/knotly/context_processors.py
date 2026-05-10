from apps.knotly.permissions import is_knotly_admin


def knotly_permissions(request):
    return {
        'knotly_can_access_dashboard': is_knotly_admin(request.user),
    }
