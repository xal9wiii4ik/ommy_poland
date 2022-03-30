import mock
import typing as tp

from django.core.files import File

from api.order.models import OrderFile
from api.order.services import create_order_files
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class OrderServicesTest(SetupAPITestCase):
    """
    Test cases for order services
    """

    def test_create_order_files(self, *args: tp.Any) -> None:
        """
        Test for func find_order_masters
        """

        order_files_count = OrderFile.objects.all().count()
        image_mock = mock.MagicMock(spec=File)
        image_mock.name = 'image.png'

        with open('api/utils/utils_tests/videoplayback.mp4', 'rb') as file:
            create_order_files(order_id=self.order_1.pk, files=[file])
            self.assertEqual(OrderFile.objects.all().count(), order_files_count + 1)

    def test_create_order_files_not_file(self, *args: tp.Any) -> None:
        """
        Test for func find_order_masters not file
        """

        order_files_count = OrderFile.objects.all().count()
        image_mock = mock.MagicMock(spec=File)
        image_mock.name = 'image.png'

        create_order_files(order_id=self.order_1.pk, files=[image_mock])
        self.assertEqual(OrderFile.objects.all().count(), order_files_count)
