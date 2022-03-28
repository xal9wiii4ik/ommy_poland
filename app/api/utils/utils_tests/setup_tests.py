import json
import boto3

from moto import mock_s3

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.master.models import Master
from api.order.models import Order, OrderStatus
from ommy_polland import settings


@mock_s3
class SetupAPITestCase(APITestCase):
    """ SetUp tests """

    def setUp(self) -> None:
        # creating stage bucket
        s3_connection = boto3.resource('s3', region_name='us-east-1')
        s3_connection.create_bucket(Bucket=settings.ORDER_BUCKET)

        # setup users and tokens
        self.password = make_password('password')
        url = reverse('authenticate:token')

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      is_staff=True,
                                                      password=self.password,
                                                      is_active=True,
                                                      email='user_1@mail.ru',
                                                      phone_number='+375292125976')
        data = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_1 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_2 = get_user_model().objects.create(username='user_2',
                                                      password=self.password,
                                                      is_active=True,
                                                      email='user_2@mail.ru',
                                                      phone_number='+375292125979')
        data = {
            'username': self.user_2.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_2 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_master_1 = get_user_model().objects.create(username='user_master_1',
                                                             password=self.password,
                                                             is_active=True,
                                                             email='user_master_1@mail.ru',
                                                             phone_number='+375292125971',
                                                             is_master=True)
        data = {
            'username': self.user_master_1.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_master_1 = f'Token ' \
                              f'{token_data["access"]}'

        self.user_master_2 = get_user_model().objects.create(username='user_master_2',
                                                             password=self.password,
                                                             is_active=True,
                                                             email='user_master_2@mail.ru',
                                                             phone_number='+375292125912',
                                                             is_master=True)
        data = {
            'username': self.user_master_2.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_master_2 = f'Token ' \
                              f'{token_data["access"]}'
        # setup masters
        self.master_1 = Master.objects.create(user=self.user_master_1,
                                              work_experience=2,
                                              longitude=14,
                                              latitude=15,
                                              city='wroclaw')
        self.master_2 = Master.objects.create(user=self.user_master_2,
                                              work_experience=10,
                                              longitude=16,
                                              latitude=17,
                                              city='wroclaw')

        # setup orders
        self.order_1 = Order.objects.create(
            number_employees=1,
            desired_time_end_work='now',
            status=OrderStatus.OPEN.value,
            city='Wroclaw',
            longitude=20,
            latitude=13
        )
        self.order_2 = Order.objects.create(
            number_employees=2,
            desired_time_end_work='not now',
            status=OrderStatus.OPEN.value,
            city='Minsk',
            longitude=10,
            latitude=8
        )