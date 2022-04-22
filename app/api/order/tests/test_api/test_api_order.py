import json
import mock
import typing as tp

from rest_framework import status
from rest_framework.reverse import reverse

from api.order.models import Order
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class OrderModelViewSetTest(SetupAPITestCase):
    """
    Test cases for order model view set
    """

    def test_get_list(self) -> None:
        """
        Test case for get list orders
        """

        url = reverse('order:order-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.filter(customer=self.user_2).count(), len(response.json()['results']))

    def test_get_list_filter_active(self) -> None:
        """
        Test case for get list active orders
        """

        url = f'{reverse("order:order-list")}?status=active'
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.json()['results']))

    def test_get_list_filter_not_active(self) -> None:
        """
        Test case for get list not active orders
        """

        url = f'{reverse("order:order-list")}?status=past'
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.json()['results']))

    def test_get_retrieve_not_owner(self) -> None:
        """
        Test case for getting retrieve order not owner
        """

        url = reverse('order:order-detail', args=(self.order_1.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_retrieve_owner(self) -> None:
        """
        Test case for getting retrieve order owner
        """

        url = reverse('order:order-detail', args=(self.order_1.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_in_city_does_not_exist(self) -> None:
        """
        Test Case for creating new order master does not exist in city
        """

        url = reverse('order:order-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        data = {
            'city': 'Minsk'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # expected_data = {'masters': 'У нас пока что нет мастеров в вашем городе'}
        # self.assertEqual(response.json(), expected_data)

    @mock.patch('api.order.tasks.order_notification.tasks.update_order_google_sheet.delay')
    @mock.patch('api.order.tasks.order_notification.tasks.send_notification_with_new_order_to_masters.delay')
    @mock.patch('api.order.tasks.order_notification.tasks.send_search_master_status_to_customer.delay')
    @mock.patch('api.telegram_bot.tasks.notifications.tasks.send_notification_with_new_order_to_order_chat.delay')
    def test_create_order(self, *args: tp.Any) -> None:
        """
        Test Case for creating new order
        """

        url = reverse('order:order-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        data = {
            'city': 'Wroclaw',
            'desired_time_end_work': 'now',
            'latitude': 20,
            'longitude': 12,
            'number_employees': 2,
            'start_time': '2022-04-03T00:00:00+01:00',
            'name': 'some name',
            'price': 20
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_order_does_not_exist(self) -> None:
        """
        Test case for cancel order does not exist order
        """

        url = reverse('order:order-cancel-order', args=(-1,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(url)
        self.assertEqual({'order': 'Заказ не найден'}, response.data)
        self.assertEqual(response.status_code, 404)

    def test_cancel_order_not_owner(self) -> None:
        """
        Test case for cancel order does not exist order
        """

        url = reverse('order:order-cancel-order', args=(self.order_2.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(url)
        self.assertEqual({'detail': 'You do not have permission to perform this action.'}, response.data)
        self.assertEqual(response.status_code, 403)

    @mock.patch('api.order.tasks.order_notification.tasks.send_masters_notification_with_cancel_order.delay')
    @mock.patch('api.telegram_bot.tasks.notifications.tasks.send_cancel_order_to_order_chat.delay')
    def test_cancel_order(self, *args: tp.Any) -> None:
        """
        Test case for cancel order
        """

        self.assertEqual('OPEN', self.order_2.status)
        url = reverse('order:order-cancel-order', args=(self.order_2.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.patch(url)
        self.assertEqual({'order': 'Заказ был отменен'}, response.data)
        self.assertEqual(response.status_code, 200)
        self.order_2.refresh_from_db()
        self.assertEqual('CANCELED', self.order_2.status)

    def test_add_does_not_exist_order_master(self) -> None:
        """
        Test case for adding master to does not exist order
        """

        url = reverse('order:order-master-acceptance', args=(-1,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(url)
        self.assertEqual({'order': 'Заказ не найден'}, response.data)
        self.assertEqual(response.status_code, 404)

    def test_add_order_master_not_master(self) -> None:
        """
        Test case for adding master to order(not master)
        """

        url = reverse('order:order-master-acceptance', args=(-1,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

    def test_add_order_master_enough(self) -> None:
        """
        Test case for adding master to order(enough masters)
        """

        url = reverse('order:order-master-acceptance', args=(self.order_1.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(url)
        self.assertEqual({'master': 'Мы уже нашли достаточное кол-во мастеров для этого заказа'}, response.data)
        self.assertEqual(response.status_code, 400)

    def test_add_order_canceled(self) -> None:
        """
        Test case for adding master to order(enough masters)
        """

        url = reverse('order:order-master-acceptance', args=(self.order_3.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(url)
        self.assertEqual({'master': 'К сожелению заказ был отменен, ожидайте остальные заказы'}, response.data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('api.order.tasks.order_notification.tasks.send_masters_info_to_customer.delay')
    def test_add_order_master(self, *args: tp.Any) -> None:
        """
        Test case for adding master to order
        """

        url = reverse('order:order-master-acceptance', args=(self.order_2.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_2)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)
        self.order_2.refresh_from_db()
        self.assertEqual('ACCEPTED', self.order_2.status)
