import typing as tp

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsStaffPermission(BasePermission):
    """
    Permission for is staff user
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return request.user.is_staff

    def has_object_permission(self, request: Request, view: tp.Any, obj: tp.Any) -> bool:
        return request.user.is_staff
