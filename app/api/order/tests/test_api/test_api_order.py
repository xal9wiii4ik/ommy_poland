import json
import mock
import typing as tp

from rest_framework import status
from rest_framework.reverse import reverse

from api.utils.utils_tests.setup_tests import SetupAPITestCase


class OrderModelViewSetTest(SetupAPITestCase):
    """
    Test cases for order model view set
    """

    def test_get_list(self) -> None:
        """
        Test case for get list files
        """

        url = reverse('order:order-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
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
        expected_data = {'masters': 'We dont have any masters in your city yet'}
        self.assertEqual(response.json(), expected_data)

    @mock.patch('api.order.tasks.order_notification.tasks.send_notification_with_new_order_to_masters.delay')
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
            'number_employees': 2
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {'masters': 'We dont have any masters in your city yet'}
        self.assertEqual(response.json(), expected_data)
