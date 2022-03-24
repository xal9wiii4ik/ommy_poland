import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TokensAPITestCase(APITestCase):
    """ Tokens tests """

    def setUp(self) -> None:
        self.password = 'password'

        self.user_1 = get_user_model().objects.create(
            username='user_1',
            password=make_password(self.password),
            phone_number='+375292125987'
        )

    def test_pair(self) -> None:
        url = reverse('token')

        data = {
            'username': self.user_1.username,
            'password': self.password
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertIsNotNone(self.client.cookies.get('refresh'))
        self.assertIsNone(response.json().get('refresh'))

    def test_refresh(self) -> None:
        url = reverse('token_refresh')
        response = self.client.post(url)
        expected_data = {'detail': 'No valid refresh token found in cookie', 'code': 'token_not_valid'}
        self.assertEqual(expected_data, response.json())
