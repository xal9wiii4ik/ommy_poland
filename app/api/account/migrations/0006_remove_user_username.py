# Generated by Django 4.0.1 on 2022-04-26 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]