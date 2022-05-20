import typing as tp

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.payments.permissions import IsStaffPermission
from api.payments.serializers import CommissionSerializer
from api.payments.services import create_commission
from api.utils.services import get_serializer_data


class CommissionApiView(APIView):
    """ Api view for creating commission """

    permission_classes = (IsAuthenticated, IsStaffPermission,)

    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=CommissionSerializer)
        create_commission(data=serializer_data)
        return Response(
            data={'commission': f'Has been created, {serializer_data["missing_pks"]} skipped'},
            status=status.HTTP_200_OK
        )
