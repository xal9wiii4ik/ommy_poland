# Generated by Django 4.0.1 on 2022-04-29 08:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0004_activateaccountcode_last_resend_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activateaccountcode',
            name='last_resend_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 29, 8, 43, 33, 863787, tzinfo=utc), null=True, verbose_name='Last resend code datetime'),
        ),
    ]
