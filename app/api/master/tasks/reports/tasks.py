import gspread
import typing as tp

from celery import shared_task

from ommy_polland import settings


@shared_task
def update_master_info_google_sheet(masters_ids: tp.List[int], start_date: str, end_date: str):
    """
    Update master info in google sheet
    Args:
        masters_ids: ids of masters
        start_date: start date for average commission
        end_date: end date for average commission
    """

    print(start_date)
    print(end_date)

    from django.db.models import Q, Sum
    from api.master.models import Master
    from api.master.serializers import MasterWorkSheetSerializer

    service_account = gspread.service_account()
    sheet = service_account.open(settings.SHEET)
    # clear all the values which were before
    sheet.values_clear(f'{settings.MASTER_WORK_SHEET}!A2:J1000')

    work_sheet = sheet.worksheet(settings.MASTER_WORK_SHEET)

    queryset = Master.objects.select_related('user').prefetch_related('master_experience').annotate(
        amount=Sum(
            'master_commission__amount',
            filter=Q(master_commission__closing_order_datetime__range=[start_date, end_date])
        ),
    ).filter(id__in=masters_ids)

    serializer = MasterWorkSheetSerializer(queryset, many=True)
    serializer_data = serializer.data

    current_column = 2
    columns_name = 'ABCDEFGHIJ'

    for data in serializer_data:
        for index, key in enumerate(data.keys()):
            work_sheet.update(f'{columns_name[index]}{current_column}',
                              data[key],
                              value_input_option="USER_ENTERED")
        current_column += 1

    work_sheet.columns_auto_resize(0, 14)
