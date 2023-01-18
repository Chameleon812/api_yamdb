from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        #return (request.user.is_authenticated and request.user.role == 'admin')
        return True


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.role == 'admin' or user.is_superuser))

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_authenticated
                and (user.role == 'admin' or user.is_superuser))
