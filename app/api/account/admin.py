from django.contrib import admin

from api.account.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    """
    Display table User on admin panel
    """

    list_display = ('id', 'first_name', 'middle_name', 'phone_number', 'is_master')
    exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions', 'password']
