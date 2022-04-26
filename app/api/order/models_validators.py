from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_less_then_forty(value):
    if value > 40:
        raise ValidationError(
            _('%(value)s should be less then 40'),
            params={'value': value},
        )


def validate_positive_number(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s should be positive'),
            params={'value': value},
        )
