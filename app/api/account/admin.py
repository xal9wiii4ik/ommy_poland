from django.contrib import admin

from api.account.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    """
    Display table User on admin panel
    """

    @staticmethod
    def name(user: User):
        return f'{user.first_name} {user.middle_name}'

    list_display = ('id', 'name', 'phone_number', 'is_master')
    exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions', 'password']
