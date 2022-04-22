import gspread
import typing as tp

from datetime import timedelta, datetime
from twilio.rest import Client

from celery import shared_task

from api.utils.tasks_utils import send_phone_message
from ommy_polland import settings


# TODO add link, update commisiya
@shared_task
def send_notification_with_new_order_to_masters(order_pk: int,
                                                masters_phone_numbers: tp.List[str],
                                                current_time: str) -> None:
    """
    Send notification with new order to masters
    Args:
        order_pk: order pk
        masters_phone_numbers: masters phone numbers
        current_time: current_time
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    order_masters = order.master.all().count()
    if order.status != 'CANCELED' and order_masters < order.number_employees:
        wait_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.%f%z') + timedelta(minutes=15)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        order_execute_time = f'{order.start_time:"%Y-%m-%dT%H:%M:%S.%f%z"}' if order.start_time is not None else 'now'
        message = f'Новая заявка!\n' \
                  f'Описание: {order.name}\n' \
                  f'Когда нужно выполнить заказ: {order_execute_time}\n' \
                  f'Предварительная цена: {order.price}\n' \
                  f'Коммисия сервиса: some 123\n' \
                  f'Стоимость без коммисии: some price\n' \
                  f'Ссылка для подтверждения: some link'

        count_of_messages_sent = 0
        for master_phone_number in masters_phone_numbers:
            _ = client.messages.create(
                to=master_phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=message
            )
            count_of_messages_sent += 1
            if count_of_messages_sent == 3:
                send_notification_with_new_order_to_masters.apply_async(
                    eta=wait_time,
                    args=(
                        1,
                        masters_phone_numbers[count_of_messages_sent:],
                        wait_time
                    )
                )
                break


# TODO add link to message
# TODO add prefetch related(N+1) if necessary needed
@shared_task
def send_masters_info_to_customer(order_pk: int) -> None:
    """
    Send phone message with masters info to customer
    Args:
        order_pk: order pk
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    masters = order.master.all()

    message = 'Мастер(а) найден(ы)\n' \
              'Информация о мастере(ах):\n'
    for master in masters:
        message += f'\tИмя мастера: {master.user.first_name} {master.user.last_name}\n' \
                   f'\tТелефон мастера: {master.user.phone_number}\n'

    send_phone_message(message=message, recipients_number=order.customer.phone_number)


# TODO add link
# TODO add logic if customer didnt click to cancel
@shared_task
def send_search_master_status_to_customer(order_pk: int, current_time: str):
    """
    Send notification with status of masters search(if not enough masters accept order or etc)
    Args:
        order_pk: order pk
        current_time: current time
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    order_masters_count = order.master.all().count()
    number_employees = order.number_employees
    current_datetime = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    link = 'link_here'
    if number_employees < order_masters_count and order.status != 'CANCELED':
        if current_datetime < order.start_time:
            message = f'Продолжается поиск мастеров.\n' \
                      f'Вы можете следить за статусом заявки на странице “Заявка”,\n' \
                      f'а также отменить заявку, если необходимо. {link}'
            task_execute_time = current_datetime + timedelta(minutes=30)
            send_search_master_status_to_customer.apply_async(eta=task_execute_time, args=(order_pk, task_execute_time))
        else:
            message = f'Не удалось найти мастера. \n' \
                      f'Вы можете продолжить поиск, если нажмете кнопку Продолжить на странице Заявки link here, ' \
                      f'или остановить поиск, если нажмете кнопку Отменить заяку {link}'
        send_phone_message(message=message, recipients_number=order.customer.phone_number)


# TODO add prefetch related(N+1) if necessary needed
@shared_task
def send_masters_notification_with_cancel_order(order_pk: int) -> None:
    """
    Send notification to masters with cancel order
    Args:
        order_pk: order pk
    """

    from api.order.models import Order

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    order = Order.objects.get(pk=order_pk)
    order_masters = order.master.all()

    message = f'Заказ {order.name}, по адресу {order.address} был отменен'

    for master in order_masters:
        _ = client.messages.create(
            to=master.user.phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )


@shared_task
def update_order_google_sheet(order_pk: int):
    """
    Update google sheet with new order
    Args:
        order_pk: order_pk
    """

    from django.db.models import F
    from api.order.models import Order
    from api.order.serializers import GoogleSheetOrderSerializer

    service_account = gspread.service_account()
    sheet = service_account.open(settings.SHEET)

    work_sheet = sheet.worksheet(settings.WORK_SHEET)

    # TODO update commission
    order = Order.objects.select_related('customer').select_related('work_sphere').annotate(
        phone_number=F('customer__phone_number'),
        work_sphere_name=F('work_sphere__name'),
        first_name=F('customer__first_name'),
    ).get(pk=order_pk)

    serializer = GoogleSheetOrderSerializer(order)
    serializer_data = serializer.data

    count_columns = len(work_sheet.get_all_values())
    current_column = count_columns + 1

    columns_name = 'BCDEFGHIJKLM'

    order_number = None
    for value in reversed(work_sheet.col_values(1)):
        if value.isnumeric():
            order_number = int(value) + 1
            break

    work_sheet.update(f'A{current_column}', order_number if order_number is not None else 1)

    for index, key in enumerate(serializer_data.keys()):
        if key == 'order_files':
            additional_columns = 0
            for file in serializer_data[key]:
                work_sheet.update(f'{columns_name[index]}{current_column + additional_columns}', file['bucket_path'])
                additional_columns += 1
        else:
            work_sheet.update(f'{columns_name[index]}{current_column}', serializer_data[key])

    work_sheet.columns_auto_resize(0, 14)
