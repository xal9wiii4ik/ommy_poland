import json
import boto3

from moto import mock_s3

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.authenticate.models import ActivateAccountCode
from api.master.models import Master, WorkSphere
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

        self.user_1 = get_user_model().objects.create(is_staff=True,
                                                      password=self.password,
                                                      is_active=True,
                                                      email='user_1@mail.ru',
                                                      phone_number='+375292125976')
        data = {
            'phone_number': self.user_1.phone_number,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_1 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_2 = get_user_model().objects.create(password=self.password,
                                                      is_active=True,
                                                      email='user_2@mail.ru',
                                                      phone_number='+375292125979')
        data = {
            'phone_number': self.user_2.phone_number,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_2 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_master_1 = get_user_model().objects.create(password=self.password,
                                                             is_active=True,
                                                             email='user_master_1@mail.ru',
                                                             phone_number='+375292125971',
                                                             is_master=True)
        data = {
            'phone_number': self.user_master_1.phone_number,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_master_1 = f'Token ' \
                              f'{token_data["access"]}'

        self.user_master_2 = get_user_model().objects.create(password=self.password,
                                                             is_active=True,
                                                             email='user_master_2@mail.ru',
                                                             phone_number='+375292125912',
                                                             is_master=True)
        data = {
            'phone_number': self.user_master_2.phone_number,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_master_2 = f'Token ' \
                              f'{token_data["access"]}'
        # setup activation codes
        self.code_1 = ActivateAccountCode.objects.create(
            user=self.user_1,
            code=5962
        )
        # setup work spheres
        self.work_sphere_1 = WorkSphere.objects.create(
            name='first'
        )
        self.work_sphere_2 = WorkSphere.objects.create(
            name='second'
        )
        # setup masters
        self.master_1 = Master.objects.create(user=self.user_master_1,
                                              longitude=14,
                                              latitude=15,
                                              city='wroclaw')
        self.master_2 = Master.objects.create(user=self.user_master_2,
                                              longitude=16,
                                              latitude=17,
                                              city='wroclaw')

        # setup orders
        self.order_1 = Order.objects.create(
            number_employees=1,
            desired_time_end_work='now',
            status=OrderStatus.SEARCH_MASTER.name,
            types_of_work=['first', 'second'],
            city='Wroclaw',
            longitude=20,
            latitude=13,
            start_time=timezone.now(),
            customer=self.user_1,
            price=20,
        )
        self.order_1_done = Order.objects.create(
            number_employees=1,
            desired_time_end_work='now',
            status=OrderStatus.DONE.name,
            types_of_work=['first', 'second'],
            city='Wroclaw',
            longitude=20,
            latitude=13,
            start_time=timezone.now(),
            customer=self.user_1,
            price=20,
        )
        self.order_1_search_master = Order.objects.create(
            number_employees=1,
            desired_time_end_work='now',
            types_of_work=['first', 'second'],
            status=OrderStatus.SEARCH_MASTER.name,
            city='Wroclaw',
            longitude=20,
            latitude=13,
            start_time=timezone.now(),
            customer=self.user_1,
            price=20,
        )
        self.order_1.master.add(self.master_1)

        self.order_2 = Order.objects.create(
            types_of_work=['first', 'second'],
            number_employees=2,
            desired_time_end_work='not now',
            status=OrderStatus.SEARCH_MASTER.name,
            city='Minsk',
            longitude=10,
            latitude=8,
            start_time=timezone.now(),
            customer=self.user_2,
            price=20,
        )
        self.order_2.master.add(self.master_1)

        self.order_3 = Order.objects.create(
            number_employees=2,
            types_of_work=['first', 'second'],
            desired_time_end_work='not now',
            status=OrderStatus.CANCELED.name,
            city='Minsk',
            longitude=10,
            latitude=8,
            start_time=timezone.now(),
            price=20,
        )
