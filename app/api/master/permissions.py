import typing as tp

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from api.master.models import Master, MasterExperience


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


class IsOwnerMasterExperiencePermission(BasePermission):
    """
    Permission for is owner for model master experience
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_master
        )

    def has_object_permission(self, request: Request, view: tp.Any, obj: MasterExperience) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj.master.user
        )
