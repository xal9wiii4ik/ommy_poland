from datetime import datetime, timedelta

from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from apps.order.serializers import OrderModelSerializer
from apps.order.models import Order
from apps.order.services_views import create_order_files
from apps.telegram_bot.tasks.notifications.tasks import (
    send_notification_with_new_order_to_order_chat,
    notification_with_coming_order,
)


class OrderCreateOnlyViewSet(CreateModelMixin,
                             GenericViewSet):
    """
    View Set for create only order
    """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs) -> Response:
        response = super(OrderCreateOnlyViewSet, self).create(request, *args, **kwargs)

        if request.FILES:
            create_order_files(files=self.request.FILES.pop('files'),
                               order_id=response.data.get('id'))
        send_notification_with_new_order_to_order_chat.delay(response.data['id'])

        if response.data.get('start_time') is not None:
            start_time = datetime.strptime(response.data.get('start_time'), "%Y-%m-%dT%H:%M:%S.%f%z")
            start_time = start_time - timedelta(hours=3, minutes=30)
            notification_with_coming_order.apply_async(eta=start_time, args=(response.data['id'],))
        return Response(data={}, status=200)

    def perform_create(self, serializer: OrderModelSerializer) -> None:
        serializer.validated_data['customer'] = self.request.user
        serializer.save()
