# Generated by Django 4.0.1 on 2022-03-22 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_experience', models.PositiveIntegerField(verbose_name='work experience')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='longitude in degrees')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='latitude in degrees')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='master', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]