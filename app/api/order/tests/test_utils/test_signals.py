from api.master.models import Master
from api.payments.models import Commission
from api.utils.utils_tests.setup_tests import SetupAPITestCase


class OrderSignalsTest(SetupAPITestCase):
    """
    Test cases for order signals
    """

    def test_m2m_commission(self) -> None:
        """ Test case for creating commission through m2m """

        commissions_count = Commission.objects.all().count()
        masters_pks = [master.pk for master in Master.objects.all()]
        self.order_3.master.add(*masters_pks)
        self.assertEqual(Commission.objects.all().count(), commissions_count + 1)
        commission = Commission.objects.get(order=self.order_3)
        self.assertEqual(len(masters_pks), commission.master.all().count())
        self.assertEqual(commission.amount, (self.order_3.price / len(masters_pks)) * 20 / 100)

    def test_recalculation_amount_add_master(self) -> None:
        """ Test case for recalculation of the amount caused by adding a new master to the order """

        commission = Commission.objects.get(order=self.order_1)
        commission_amount = commission.amount
        self.order_1.master.add(self.master_2)

        commission.refresh_from_db()
        self.order_1.refresh_from_db()

        self.assertNotEqual(commission_amount, commission.amount)
        self.assertEqual(
            [master.pk for master in commission.master.all()], [master.pk for master in self.order_1.master.all()]
        )

    def test_recalculation_amount_remove_master(self) -> None:
        """ Test case for recalculation of the amount caused by removing the master from the order """

        commission = Commission.objects.get(order=self.order_1)
        commission_amount = commission.amount
        self.order_1.master.add(self.master_2)
        self.order_1.master.remove(self.master_2)

        commission.refresh_from_db()
        self.order_1.refresh_from_db()

        self.assertNotEqual(commission_amount, commission.amount)
        self.assertEqual(
            [master.pk for master in commission.master.all()], [master.pk for master in self.order_1.master.all()]
        )
