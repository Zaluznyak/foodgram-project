from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        sufficient_conditions = (
            obj.author == user,
            user.is_admin
        )
        return any(sufficient_conditions)
