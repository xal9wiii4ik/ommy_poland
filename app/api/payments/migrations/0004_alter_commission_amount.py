# Generated by Django 4.0.1 on 2022-05-31 15:16

import api.order.models_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_remove_commission_master_commission_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[api.order.models_validators.validate_positive_number], verbose_name='Commission amount'),
        ),
    ]
