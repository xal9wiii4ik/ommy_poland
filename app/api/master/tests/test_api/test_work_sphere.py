from rest_framework import status
from rest_framework.reverse import reverse

from api.utils.utils_tests.setup_tests import SetupAPITestCase


class TestWorkSphereModelViewSetTest(SetupAPITestCase):
    """ Tests for WorkSphereModelViewSet """

    def test_get(self) -> None:
        url = reverse('master:worksphere-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
