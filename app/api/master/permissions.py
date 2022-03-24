import typing as tp

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from django.db.models import Model


class IsOwnerMasterPermission(BasePermission):
    """
    Permission for staff or teacher or view for all users
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return True

    def has_object_permission(self, request: Request, view: tp.Any, obj: Model) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj
        )
