# Generated by Django 4.0.1 on 2022-04-27 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_master_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='middle_name',
        ),
    ]