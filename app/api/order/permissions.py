import typing as tp

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsMasterPermission(BasePermission):
    """
    Permission for is master
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return request.user.is_authenticated and request.user.is_master
