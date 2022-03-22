from rest_framework.exceptions import ValidationError, ErrorDetail

from apps.account.serializers import UserRegisterSerializer
from apps.utils.setup_tests import SetupAPITestCase


class RegisterUserTestCase(SetupAPITestCase):
    """
    Test Case for serializer register user
    """

    def test_exist_phone_number(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'some@email.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '+375292125978'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'phone_number': [ErrorDetail(string="{'User with this phone number already exist'}", code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_invalid_phone_number(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'some@email.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '375292125978'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'phone_number': [ErrorDetail(string="{'Invalid phone number, example: +375*********'}", code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_exist_email(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'user_1@mail.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '+375292125921'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'email': [ErrorDetail(string="{'User with this email already exist'}", code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_invalid_email(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'someemail.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '+375292125921'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_not_equal_repeat_password(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakml2',
                'email': 'user_11@mail.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '+375292125921'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'repeat_password': [ErrorDetail(string='Repeat password should be equal to password', code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_username(self) -> None:
        data = {
            'password': 'aksjdakmdl2',
            'repeat_password': 'aksjdakmdl2',
            'email': 'user_11@mail.ru',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone_number': '+375292125921'
        }
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        self.assertEqual('+375292125921', serializer_data['username'])
