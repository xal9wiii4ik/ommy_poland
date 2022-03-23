# Generated by Django 4.0.1 on 2022-02-28 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9, verbose_name='latitude in degrees'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9, verbose_name='longitude in degrees'),
            preserve_default=False,
        ),
    ]