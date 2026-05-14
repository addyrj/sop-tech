def sync_permissions(source_user, target_user):
    target_user.user_permissions.set(source_user.user_permissions.all())
    target_user.groups.set(source_user.groups.all())
    target_user.save()