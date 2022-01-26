from django.contrib import admin

from apps.account.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    """
    Display table User on admin panel
    """

    list_display = ('pk', 'username', 'email', 'phone_number', 'address')
