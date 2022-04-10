from twilio.rest import Client

from ommy_polland import settings


def send_phone_message(message: str, recipients_number: str) -> None:
    """
    Send phone message
    Args:
        message: message
        recipients_number: recipient's number
    """

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    _ = client.messages.create(
        to=recipients_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )
