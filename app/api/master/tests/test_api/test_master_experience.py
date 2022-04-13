import json

from rest_framework import status
from rest_framework.reverse import reverse

from api.utils.utils_tests.setup_tests import SetupAPITestCase


class TestMasterExperienceModelViewSetTest(SetupAPITestCase):
    """ Tests for TestMasterExperience """

    def test_get(self) -> None:
        url = reverse('master:masterexperience-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self) -> None:
        url = reverse('master:masterexperience-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_master_2)
        data = {
            'work_sphere': self.work_sphere_1.pk,
            'experience': 123
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_not_master(self) -> None:
        url = reverse('master:masterexperience-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        data = {
            'work_sphere': self.work_sphere_1.pk,
            'experience': 123
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
