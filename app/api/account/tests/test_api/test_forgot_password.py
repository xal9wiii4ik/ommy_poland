import json

from rest_framework.reverse import reverse

from api.authenticate.models import ActivateAccountCode
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class UpdatePasswordTest(SetupAPITestCase):
    """
    Test cases for update password
    """

    def test_update_password(self) -> None:
        activating_codes_count = ActivateAccountCode.objects.all().count()
        url = reverse('account:update_password')
        data = {
            'code': self.code_1.code,
            'password': 'password_1',
            'repeat_password': 'password_1'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ActivateAccountCode.objects.all().count(), activating_codes_count - 1)
        first_access = response.data['access']
        url_1 = reverse('authenticate:token_refresh')
        response_1 = self.client.post(url_1)
        second_access = response_1.data['access']
        self.assertNotEqual(first_access, second_access)
        self.assertIsNotNone(self.client.cookies.get('refresh'))
