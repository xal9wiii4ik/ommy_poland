import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.authenticate.models import ActivateAccountCode
from api.authenticate.tests.test_serializers.test_resend_code import ResendCodeSetUp


class TokensAPITestCase(APITestCase):
    """ Tokens tests """

    def setUp(self) -> None:
        self.password = 'password'

        self.user_1 = get_user_model().objects.create(
            password=make_password(self.password),
            phone_number='+375292125976'
        )

    def test_pair(self) -> None:
        url = reverse('authenticate:token')
        url_1 = reverse('authenticate:token_refresh')

        data = {
            'phone_number': self.user_1.phone_number,
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
            password=make_password(self.password),
            phone_number='+375292125976',
            is_active=False
        )
        self.code = ActivateAccountCode.objects.create(user=self.user_1, code=1234)

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
        self.assertIsNotNone(self.client.cookies.get('refresh'))
        self.assertIsNone(response.json().get('refresh'))

    def test_activate_account_not_valid(self) -> None:
        """
        Test Activate account not valid code
        """

        url = reverse('authenticate:activate')
        data = {
            'user_pk': self.user_1.pk,
            'code': 1982
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'code': ['code with this user does not exist']})
        self.assertIsNone(self.client.cookies.get('refresh'))
        self.assertIsNone(response.json().get('refresh'))


class ResendingActivatingCodeApiViewTestCase(ResendCodeSetUp):
    """ Test case for ResendingActivatingCodeApiView """

    def test_valid(self) -> None:
        url = reverse('authenticate:resend_code')
        data = {'user_pk': self.user.pk}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'code': 'Код был отправлен'})


class CheckActivationCodeApiViewTestCase(ResendCodeSetUp):
    """ Test Case for CheckActivationCodeApiView """

    def test_valid(self) -> None:
        url = reverse('authenticate:check_activation_code')
        data = {'code': self.code.code}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_not_valid(self) -> None:
        url = reverse('authenticate:check_activation_code')
        data = {'code': 9876}
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.json(), {'code': ['Не верный код активации']})
        self.assertEqual(response.status_code, 400)
