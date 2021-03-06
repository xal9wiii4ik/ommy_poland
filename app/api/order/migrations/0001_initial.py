# Generated by Django 4.0.1 on 2022-03-22 17:06

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name of order')),
                ('number_employees', models.IntegerField(verbose_name='number of employees')),
                ('desired_time_end_work', models.CharField(max_length=10, verbose_name='desired time end of work')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='work start time')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Order price')),
                ('description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Description of order')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='Address of the customer')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('OPEN', 'open'), ('ACCEPTED', 'accepted'), ('IN_PROGRESS', 'in_progress'), ('DONE', 'done'), ('PAID', 'paid'), ('CANCELED', 'canceled')], default='open', max_length=30)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='longitude in degrees')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='latitude in degrees')),
                ('types_of_work', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None, verbose_name='types of work')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkSphere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='work sphere')),
            ],
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bucket_path', models.CharField(max_length=1056, verbose_name='Bucket path')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_files', to='order.order', verbose_name='Order')),
            ],
            options={
                'db_table': 'order_file',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='work_sphere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_work_sphere', to='order.worksphere', verbose_name='order work sphere'),
        ),
    ]
