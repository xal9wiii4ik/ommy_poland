from rest_framework.exceptions import ValidationError, ErrorDetail

from api.account.serializers import UserRegisterSerializer
from api.utils.utils_tests.setup_tests import SetupAPITestCase


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
                'phone_number': '+375292125978',
                'middle_name': 'middle'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'phone_number': [ErrorDetail(
                    string='Пользователь с таким номером телефона уже заругистрирован',
                    code='invalid'
                )]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_invalid_password(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2фыв',
                'repeat_password': 'aksjdakmdl2фыв',
                'email': 'some@email.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'phone_number': '+375292105978',
                'middle_name': 'middle'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'password': [ErrorDetail(string='Пароль должен содержать латинские буквы и цыфры', code='invalid')]
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
                'phone_number': '375292125978',
                'middle_name': 'middle'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'phone_number': [ErrorDetail(string='Неверный номер телефона, пример: +375*********', code='invalid')]
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
                'phone_number': '+375292125921',
                'middle_name': 'middle'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'email': [ErrorDetail(string='Пользователь с такой почтой уже зарегистрирован', code='invalid')]
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
                'phone_number': '+375292125921',
                'middle_name': 'middle'
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
                'phone_number': '+375292125921',
                'middle_name': 'middle'
            }
            serializer = UserRegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'repeat_password': [ErrorDetail(string='repeat_password должен быть равен password', code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)
