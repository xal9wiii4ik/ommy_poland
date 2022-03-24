from django.contrib import admin

from api.master.models import Master


@admin.register(Master)
class MasterModelAdmin(admin.ModelAdmin):
    """
    Display table Master on admin panel
    """

    list_display = ('pk', 'user', 'longitude', 'latitude', 'city', 'work_experience')
