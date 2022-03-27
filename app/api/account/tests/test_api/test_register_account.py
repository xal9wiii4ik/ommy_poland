import json
import mock
import typing as tp

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from api.authenticate.models import ActivateAccountCode
from api.utils.setup_tests import SetupAPITestCase


class RegisterAccountTest(SetupAPITestCase):
    """
    Test cases for register account
    """

    @mock.patch('api.authenticate.tasks.activate_user.tasks.send_phone_activate_message.delay')
    def test_register_account(self, *args: tp.List[tp.Any]) -> None:
        codes_count = ActivateAccountCode.objects.all().count()
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
        # checking if mock is working
        self.assertEqual(ActivateAccountCode.objects.all().count(), codes_count)
