# Generated by Django 4.0.1 on 2022-03-06 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_master_latitude_master_longitude'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='master',
            options={},
        ),
        migrations.AlterModelTable(
            name='master',
            table='master',
        ),
    ]
