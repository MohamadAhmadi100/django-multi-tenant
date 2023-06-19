from rest_framework import permissions
from rest_framework_auth0.permissions import (
    HasGroupBasePermission,
    HasRoleBasePermission,
    HasPermissionBasePermission
)


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class HasAdminGroupPermission(HasGroupBasePermission):
    group_name = 'admins'


class HasAdminRolePermission(HasRoleBasePermission):
    role_name = 'admin'


class CanReadToDosPermission(HasPermissionBasePermission):
    permission_name = 'read:documents'
