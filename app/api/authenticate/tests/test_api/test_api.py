import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.authenticate.models import ActivateAccountCode


class TokensAPITestCase(APITestCase):
    """ Tokens tests """

    def setUp(self) -> None:
        self.password = 'password'

        self.user_1 = get_user_model().objects.create(
            username='user_1',
            password=make_password(self.password),
            phone_number='+375292125976'
        )

    def test_pair(self) -> None:
        url = reverse('authenticate:token')
        url_1 = reverse('authenticate:token_refresh')

        data = {
            'username': self.user_1.username,
            'password': self.password
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertIsNotNone(self.client.cookies.get('refresh'))
        self.assertIsNone(response.json().get('refresh'))
        response_1 = self.client.post(url_1)
        expected_data = {'detail': 'No valid refresh token found in cookie', 'code': 'token_not_valid'}
        self.assertNotEqual(expected_data, response_1.json())

    def test_refresh(self) -> None:
        url = reverse('authenticate:token_refresh')
        response = self.client.post(url)
        expected_data = {'detail': 'No valid refresh token found in cookie', 'code': 'token_not_valid'}
        self.assertEqual(expected_data, response.json())


class ActivateAccountAPITestCase(APITestCase):
    """
    Test activate account view
    """

    def setUp(self) -> None:
        self.password = 'password'

        self.user_1 = get_user_model().objects.create(
            username='user_1',
            password=make_password(self.password),
            phone_number='+375292125976',
            is_active=False
        )
        self.code = ActivateAccountCode.objects.create(user=self.user_1, code=123456)

    def test_activate_account(self) -> None:
        """
        Test Activate account
        """

        self.assertEqual(ActivateAccountCode.objects.all().count(), 1)
        self.assertFalse(self.user_1.is_active)
        url = reverse('authenticate:activate')
        data = {
            'user_pk': self.user_1.pk,
            'code': self.code.code
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ActivateAccountCode.objects.all().count(), 0)
        self.user_1.refresh_from_db()
        self.assertTrue(self.user_1.is_active)
