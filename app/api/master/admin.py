from django.contrib import admin

from apps.master.models import Master


@admin.register(Master)
class MasterModelAdmin(admin.ModelAdmin):
    """
    Display table Master on admin panel
    """

    list_display = ('pk', 'username', 'email', 'phone_number', 'address', 'longitude', 'latitude', 'city')
