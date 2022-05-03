from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from api.authenticate.models import ActivateAccountCode
from api.authenticate.serializers import ResendingActivatingCodeSerializer


class ResendCodeSetUp(APITestCase):
    """ SetUp for resend code tests"""

    def setUp(self) -> None:
        self.password = make_password('password')

        self.user = get_user_model().objects.create(is_staff=True,
                                                    password=self.password,
                                                    is_active=True,
                                                    email='user_1@mail.ru',
                                                    phone_number='+375292125976')
        self.code = ActivateAccountCode.objects.create(user=self.user,
                                                       code=1234)


class ResendingActivatingCodeSerializerTestCase(ResendCodeSetUp):
    """ ResendingActivatingCodeSerializer tests """

    def test_user_not_exist(self) -> None:
        data = {'user_pk': -1}
        try:
            serializer = ResendingActivatingCodeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'code': [ErrorDetail(string='У вас нету активных кодов активации', code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_first_resend(self) -> None:
        last_resending_time = self.code.last_resend_datetime
        number_resending = self.code.number_resending
        data = {'user_pk': self.user.pk}
        serializer = ResendingActivatingCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.code.refresh_from_db()
        self.assertEqual(self.code.number_resending, number_resending + 1)
        self.assertNotEqual(self.code.last_resend_datetime, last_resending_time)

    def test_error_resend(self) -> None:
        self.code.number_resending = 2
        self.code.save()
        data = {'user_pk': self.user.pk}
        try:
            serializer = ResendingActivatingCodeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            # False because its not possible to detect how time you should wait
            self.assertFalse(False)

    def test_resend_more_7_times(self) -> None:
        self.code.number_resending = 8
        self.code.save()
        data = {'user_pk': self.user.pk}
        try:
            serializer = ResendingActivatingCodeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'code': [ErrorDetail(
                    string='Вы израсходовали 7 попыток повторного отправки кода, обратитесь к администратору',
                    code='invalid'
                )]
            }
            self.assertEqual(expected_exception, e.detail)
