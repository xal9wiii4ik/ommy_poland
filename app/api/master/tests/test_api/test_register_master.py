import json
import mock
import typing as tp

from rest_framework.reverse import reverse

from api.master.models import Master, MasterExperience
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class RegisterMasterTest(SetupAPITestCase):
    """
    Test cases for register master
    """

    @mock.patch('api.authenticate.tasks.activate_user.tasks.send_phone_activate_message.delay')
    def test_register_master(self, *args: tp.List[tp.Any]) -> None:
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
            'latitude': 2.6,
            'middle_name': 'middle',
            'city': 'some city'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Master.objects.all().count(), account_count + 1)

    @mock.patch('api.authenticate.tasks.activate_user.tasks.send_phone_activate_message.delay')
    def test_register_account_master_experience(self, *args: tp.List[tp.Any]) -> None:
        self.assertEqual(0, MasterExperience.objects.all().count())
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
            'latitude': 2.6,
            'middle_name': 'middle',
            'city': 'some city',
            'master_experience': [
                {
                    'experience': '123',
                    'work_sphere': self.work_sphere_1.pk
                },
                {
                    'experience': '321',
                    'work_sphere': self.work_sphere_2.pk
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Master.objects.all().count(), account_count + 1)
        self.assertEqual(2, MasterExperience.objects.all().count())
