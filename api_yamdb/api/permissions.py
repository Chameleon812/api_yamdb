from rest_framework import permissions
from reviews.models import RoleChoices


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == RoleChoices.ADMIN)


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.role == RoleChoices.ADMIN or user.is_superuser))


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == RoleChoices.ADMIN
            or request.user.role == RoleChoices.MODARATOR
            or request.user == obj.author
        )
