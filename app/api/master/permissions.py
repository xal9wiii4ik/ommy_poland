import typing as tp

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from api.master.models import Master


class IsOwnerMasterPermission(BasePermission):
    """
    Permission for is owner for model master
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return True

    def has_object_permission(self, request: Request, view: tp.Any, obj: Master) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj.user
        )
