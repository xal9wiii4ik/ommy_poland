# Generated by Django 4.0.1 on 2022-03-14 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_alter_master_options_alter_master_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='city',
            field=models.CharField(default='wroclaw', max_length=100, verbose_name='city'),
            preserve_default=False,
        ),
    ]