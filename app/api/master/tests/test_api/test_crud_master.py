
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
        expected_data = [
            {
                'id': self.master_1.pk,
                'work_experience': 2,
                'longitude': '14.000000',
                'latitude': '15.000000',
                'city': 'Wroclaw',
                'user': self.user_master_1.pk
            },
            {
                'id': self.master_2.pk,
                'work_experience': 10,
                'longitude': '16.000000',
                'latitude': '17.000000',
                'city': 'Wroclaw',
                'user': self.user_master_2.pk
            }
        ]
        self.assertEqual(response.json()['results'], expected_data)

    def test_get_retrieve(self) -> None:
        """
        Test get list of masters
        """

        url = reverse('master:master-detail', args=(self.master_1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.master_1.pk,
            'work_experience': 2,
            'longitude': '14.000000',
            'latitude': '15.000000',
            'city': 'Wroclaw',
            'user': self.user_master_1.pk
        }
        self.assertEqual(response.json(), expected_data)
