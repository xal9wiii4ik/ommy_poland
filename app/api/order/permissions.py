import typing as tp

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from api.order.models import Order


class IsMasterPermission(BasePermission):
    """
    Permission for is master
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return request.user.is_authenticated and request.user.is_master


class IsCustomerPermission(BasePermission):
    """
    Permission for is customer
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: tp.Any, obj: Order) -> bool:
        return obj.customer == request.user
