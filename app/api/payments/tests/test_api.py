import json

from rest_framework import status
from rest_framework.reverse import reverse

from api.payments.models import Commission
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class ApiViewTest(SetupAPITestCase):
    """ Test cases for api """

    def test_create_commission(self) -> None:
        count_commissions = Commission.objects.all().count()
        url = reverse('payments:create_commission')
        data = {
            'masters_pks': [self.master_1.pk, self.master_2.pk, self.master_1.pk + 100],
            'order_pk': self.order_1.pk
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.data, {'commission': 'Has been created, [101] skipped'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(Commission.objects.first().amount), 2.0)
        self.assertEqual(Commission.objects.all().count(), count_commissions + 1)

    def test_create_commission_not_staff(self) -> None:
        count_commissions = Commission.objects.all().count()
        url = reverse('payments:create_commission')
        data = {
            'masters_pks': [self.master_1.pk, self.master_2.pk, self.master_1.pk + 100],
            'order_pk': self.order_1.pk
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Commission.objects.all().count(), count_commissions)

    def test_create_commission_bad_order_pk(self) -> None:
        url = reverse('payments:create_commission')
        data = {
            'masters_pks': [self.master_1.pk, self.master_2.pk, self.master_1.pk + 100],
            'order_pk': 0
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_commission_bad_master_pk(self) -> None:
        url = reverse('payments:create_commission')
        data = {
            'masters_pks': [0, 0, self.master_1.pk + 100],
            'order_pk': 0
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(path=url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
