import json

from rest_framework import status
from rest_framework.reverse import reverse

from api.utils.utils_tests.setup_tests import SetupAPITestCase


class TestMasterModelViewSetTest(SetupAPITestCase):
    """
    Test cases for master model view set
    """

    def test_get_list(self) -> None:
        """
        Test get list of masters
        """

        url = reverse('master:master-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_retrieve(self) -> None:
        """
        Test get list of masters
        """

        url = reverse('master:master-detail', args=(self.master_1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_master_account_not_owner(self) -> None:
        url = reverse('master:master-detail', args=(self.master_1.pk,))
        data = {'data': 'data'}
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_2)
        response = self.client.patch(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_master_account_owner(self) -> None:
        user_pk = self.master_1.user.pk
        longitude = self.master_1.longitude
        url = reverse('master:master-detail', args=(self.master_1.pk,))
        data = {
            'user': 1,
            'longitude': 123,
            'latitude': 124
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_1)
        response = self.client.patch(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.master_1.refresh_from_db()
        self.assertEqual(user_pk, self.master_1.user.pk)
        self.assertNotEqual(longitude, self.master_1.longitude)
