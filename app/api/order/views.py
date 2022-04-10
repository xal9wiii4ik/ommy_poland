import typing as tp

from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from api.order.permissions import IsMasterPermission, IsCustomerPermission
from api.order.serializers import OrderModelSerializer
from api.order.models import Order
from api.order.services import (
    create_order_files,
    master_exist_in_city,
    add_master_to_order,
    find_order_masters,
    get_order_or_404, cancel_order,
)
from api.order.tasks.order_notification.tasks import send_search_master_status_to_customer
from api.telegram_bot.tasks.notifications.tasks import (
    send_notification_with_new_order_to_order_chat,
)


class OrderCreateOnlyViewSet(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             GenericViewSet):
    """
    View Set for create only order
    """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsAuthenticated,)

    def create(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        # check if master exist in oder city
        if request.data.get('city') is None:
            return Response(data={'city': 'Field is required'}, status=status.HTTP_400_BAD_REQUEST)
        masters = master_exist_in_city(city=request.data['city'])
        if not masters:
            return Response(
                data={'masters': 'У нас пока что нет мастеров в вашем городе'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create order and order file and send notification
        response = super(OrderCreateOnlyViewSet, self).create(request, *args, **kwargs)

        order = Order.objects.get(pk=response.data.get('id'))

        if request.FILES:
            create_order_files(files=self.request.FILES.pop('files'),
                               order=order)

        send_notification_with_new_order_to_order_chat.delay(response.data['id'])

        current_time = timezone.now()
        status_execute_time = current_time + timedelta(minutes=30)
        send_search_master_status_to_customer.apply_async(eta=status_execute_time, args=(order.pk, status_execute_time))

        # create queue and send notifications to masters
        masters_queue_info = find_order_masters(order_pk=response.data['id'],
                                                order_longitude=float(request.data['longitude']),
                                                order_latitude=float(request.data['latitude']),
                                                masters=masters)
        response.data.update(masters_queue_info)

        # TODO update or remove
        # # send coming notification if start time not now
        # if response.data.get('start_time') is not None:
        #     start_time = datetime.strptime(response.data.get('start_time'), '%Y-%m-%dT%H:%M:%S.%f%z')
        #     start_time = start_time - timedelta(hours=3, minutes=30)
        #     notification_with_coming_order.apply_async(eta=start_time, args=(response.data['id'],))
        return response

    @action(detail=True,
            methods=['PATCH'],
            permission_classes=[IsMasterPermission],
            url_path=r'master_acceptance')
    def master_acceptance(self, request: Request, pk: int):
        order = get_order_or_404(order_pk=pk)
        if isinstance(order, Order):
            response_message, response_status = add_master_to_order(order=order, user=request.user)
            return Response(data={'master': response_message}, status=response_status)
        return Response(data={'order': 'Заказ не найден'}, status=order)

    @action(detail=True,
            methods=['PATCH'],
            permission_classes=[IsCustomerPermission],
            url_path=r'cancel_order')
    def cancel_order(self, request: Request, pk: int) -> Response:
        order = get_order_or_404(order_pk=pk)
        if isinstance(order, Order):
            response_data, responses_status = cancel_order(order=order, request=request, view_name=self.get_view_name())
            return Response(data=response_data, status=responses_status)
        return Response(data={'order': 'Заказ не найден'}, status=order)

    def perform_create(self, serializer: OrderModelSerializer) -> None:
        serializer.validated_data['customer'] = self.request.user
        serializer.save()
