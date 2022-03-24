import json

from rest_framework.reverse import reverse

from apps.master.models import Master
from apps.utils.setup_tests import SetupAPITestCase


class RegisterMasterTest(SetupAPITestCase):
    """
    Test cases for register master
    """

    def test_register_account(self) -> None:
        account_count = Master.objects.all().count()

        url = reverse('master:register')
        data = {
            'password': 'aksjdakmdl2',
            'repeat_password': 'aksjdakmdl2',
            'email': 'some@email.ru',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone_number': '+375292125918',
            'work_experience': 2,
            'longitude': 2.5,
            'latitude': 2.6
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Master.objects.all().count(), account_count + 1)
