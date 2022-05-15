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

    fields = ('last_login', 'first_name', 'last_name', 'middle_name',
              'email', 'phone_number', 'address', 'is_master',
              'is_active', 'date_joined',)
    list_display = ('id', 'name', 'phone_number', 'is_master')
    exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions', 'password']
