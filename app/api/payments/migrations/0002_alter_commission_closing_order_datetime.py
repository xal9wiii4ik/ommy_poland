# Generated by Django 4.0.1 on 2022-06-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_squashed_0005_alter_commission_closing_order_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='closing_order_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Closing order date'),
        ),
    ]
