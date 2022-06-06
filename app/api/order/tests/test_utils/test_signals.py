from django.utils import timezone

from api.master.models import Master
from api.order.models import Order, OrderStatus
from api.payments.models import Commission
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class OrderSignalsTest(SetupAPITestCase):
    """
    Test cases for order signals
    """

    def test_creating_commission(self) -> None:
        """ Test case for creating commission when an order created with the status DONE """

        commissions_count = Commission.objects.all().count()
        order = Order.objects.create(
            types_of_work=['first', 'second'],
            number_employees=2,
            desired_time_end_work='not now',
            status=OrderStatus.DONE.name,
            city='Minsk',
            longitude=10,
            latitude=8,
            start_time=timezone.now(),
            customer=self.user_2,
            price=20,
        )
        masters_pks = [master.pk for master in Master.objects.all()]
        order.master.add(*masters_pks)
        self.assertEqual(Commission.objects.all().count(), commissions_count + 1)
        commission = Commission.objects.get(order=order)
        self.assertEqual(len(masters_pks), commission.master.all().count())
        self.assertEqual(commission.amount, (order.price / len(masters_pks)) * 20 / 100)

    def test_recalculation_amount_add_master(self) -> None:
        """ Test case for recalculation of the amount caused by adding a new master to the order """

        commission = Commission.objects.get(order=self.order_1_done)
        self.order_1_done.master.add(self.master_2)

        commission.refresh_from_db()
        self.order_1_done.refresh_from_db()

        masters_pks = [master.pk for master in commission.master.all()]
        self.assertEqual(commission.amount, (self.order_1_done.price / len(masters_pks)) * 20 / 100)
        self.assertEqual(
            masters_pks, [master.pk for master in self.order_1_done.master.all()]
        )

    def test_recalculation_amount_remove_master(self) -> None:
        """ Test case for recalculation of the amount caused by removing the master from the order """

        commission = Commission.objects.get(order=self.order_1_done)
        commission_amount = commission.amount
        self.order_1.master.add(self.master_2)
        self.order_1.master.remove(self.master_2)

        commission.refresh_from_db()
        self.order_1.refresh_from_db()

        self.assertEqual(commission_amount, commission.amount)
        self.assertEqual(
            [master.pk for master in commission.master.all()], [master.pk for master in self.order_1_done.master.all()]
        )
