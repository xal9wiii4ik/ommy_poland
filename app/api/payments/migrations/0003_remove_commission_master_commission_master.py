# Generated by Django 4.0.1 on 2022-05-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_remove_master_middle_name'),
        ('payments', '0002_commission_closing_order_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='master',
        ),
        migrations.AddField(
            model_name='commission',
            name='master',
            field=models.ManyToManyField(related_name='master_commission', to='master.Master', verbose_name='Master'),
        ),
    ]