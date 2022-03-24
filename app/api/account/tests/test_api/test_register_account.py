import json

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from apps.utils.setup_tests import SetupAPITestCase


class RegisterAccountTest(SetupAPITestCase):
    """
    Test cases for register account
    """

    def test_register_account(self) -> None:
        account_count = get_user_model().objects.all().count()

        url = reverse('account:register')
        data = {
            'password': 'aksjdakmdl2',
            'repeat_password': 'aksjdakmdl2',
            'email': 'some@email.ru',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone_number': '+375292125918'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_user_model().objects.all().count(), account_count + 1)
