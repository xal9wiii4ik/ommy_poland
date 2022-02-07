import typing as tp
import logging
import boto3
import fleep

from apps.order.models import Order, OrderFile

from ommy_polland.settings import ORDER_BUCKET, BUCKET_REGION


def create_order_files(order_id: int, files: tp.List[tp.IO]) -> None:
    """ Func for saving pictures in database
    Args:
        order_id: post id
        files: list with files
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(ORDER_BUCKET)
    order = Order.objects.get(pk=order_id)

    for file in files:
        file_bytes = file.read()
        file_info = fleep.get(file_bytes)

        if not any(file_info.mime):
            logging.warning(msg=f'Something was wrong with file for order: {order_id}')
            continue

        file_path = f'{order_id}/{file.name}'
        file = bucket.put_object(Key=file_path,
                                 Body=file_bytes)
        bucket_path = f'https://s3-{BUCKET_REGION}.amazonaws.com/{ORDER_BUCKET}/{file.key}'  # type: ignore
        OrderFile.objects.create(order=order, bucket_path=bucket_path)
