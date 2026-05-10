def is_knotly_admin(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return user.groups.filter(name='Corporate Admin').exists()
