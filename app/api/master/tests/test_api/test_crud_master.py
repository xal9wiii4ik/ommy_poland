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
