from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase

from api.authenticate.models import ActivateAccountCode
from api.authenticate.tasks.activate_user.tasks import send_phone_activate_message


class AuthenticateTasksAPITestCase(APITestCase):
    """
    Test authenticate tasks
    """

    def setUp(self) -> None:
        self.password = 'password'

        self.user_1 = get_user_model().objects.create(
            username='user_1',
            password=make_password(self.password),
            phone_number='+375292125976'
        )

    def test_send_phone_activate_message(self) -> None:
        """
        Test case for send activate message to phone and test if credentials are current
        Checking whether a new code has been created and whether a message is coming to my number
        """

        self.assertEqual(ActivateAccountCode.objects.all().count(), 0)
        send_phone_activate_message(user_pk=self.user_1.pk)
        self.assertEqual(ActivateAccountCode.objects.all().count(), 1)
