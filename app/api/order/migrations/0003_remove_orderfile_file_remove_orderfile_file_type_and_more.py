# Generated by Django 4.0.1 on 2022-02-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderfile',
            name='file',
        ),
        migrations.RemoveField(
            model_name='orderfile',
            name='file_type',
        ),
        migrations.AddField(
            model_name='orderfile',
            name='bucket_path',
            field=models.CharField(default='', max_length=1056, verbose_name='Bucket path'),
            preserve_default=False,
        ),
    ]