from rest_framework import permissions


class IsBlogOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user if not request.user.is_anonymous else False

        if request.method in permissions.SAFE_METHODS:
            return False

        return user and user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user if not request.user.is_anonymous else False

        if request.method in permissions.SAFE_METHODS:
            return True

        return user and user.is_admin


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user if not request.user.is_anonymous else False

        if request.method in permissions.SAFE_METHODS:
            return True

        return user and user.is_staff


class IsAccountOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return obj.username == request.user.username


class IsStaffOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user if not request.user.is_anonymous else False

        if request.method == 'POST':
            return True

        return user and user.is_staff


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class PostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


class AccountPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'POST', 'OPTIONS', 'HEAD'):
            return True

        if request.user.is_anonymous:
            return False

        user = request.user

        if user.is_staff:
            return True

        return obj.username == user.username


class MyAccountPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return not request.user.is_anonymous

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class PostCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False

        user = request.user

        return user.is_staff


class PostReactionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.author.username == request.user.username


class PostCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        return not user.is_anonymous

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return False

        user = request.user

        is_user_privileged = user.is_staff

        return is_user_privileged or (obj.author.username == request.user.username)

