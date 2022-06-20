from rest_framework.test import APITestCase
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from ommy_polland import settings


class TestTwilio(APITestCase):
    def test_bad_connection(self) -> None:
        client = Client(f'{settings.TWILIO_ACCOUNT_SID}as', settings.TWILIO_AUTH_TOKEN)
        try:
            client.balance.fetch()
            self.assertTrue(False)
        except TwilioRestException:
            self.assertTrue(True)

    def test_connection(self) -> None:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.balance.fetch()
        self.assertTrue(True)
