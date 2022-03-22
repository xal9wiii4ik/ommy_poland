from django.contrib import admin

from api.authenticate.models import ActivateAccountCode


@admin.register(ActivateAccountCode)
class ActivateAccountCodesModelAdmin(admin.ModelAdmin):
    """
    Display table ActivateAccountCodes on admin panel
    """

    list_display = ['pk', 'code', 'user']
