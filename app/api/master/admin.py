import typing as tp

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.master.forms import DateRangeForm
from api.master.models import Master, MasterExperience, WorkSphere
from api.master.tasks.reports.tasks import update_master_info_google_sheet


@admin.register(Master)
class MasterModelAdmin(admin.ModelAdmin):
    """ Display table Master on admin panel """

    @staticmethod
    def work_experiences(obj: Master):
        message = ''
        for experience in obj.master_experience.all():
            message += f'<div>sphere_name: {experience.work_sphere.name}</div>' \
                       f'<div>years: {experience.experience}</div>' \
                       f'<p>'
        return mark_safe(message)

    @staticmethod
    def move_to_user(obj: Master):
        link = reverse('admin:account_user_change', args=[obj.user.pk])
        return mark_safe(f'<a href="{link}">User</a>')

    list_display = ('id', 'city', 'work_experiences', 'move_to_user')
    readonly_fields = ('longitude', 'latitude',)

    actions = ['report_commission_amount']

    def report_commission_amount(
            self, request: WSGIRequest,
            queryset: QuerySet) -> tp.Union[render, HttpResponseRedirect]:
        if 'apply' in request.POST:
            form = DateRangeForm(request.POST)

            if form.is_valid():
                update_master_info_google_sheet.delay(
                    [master.pk for master in queryset],
                    form.cleaned_data['start'],
                    form.cleaned_data['end']
                )
            self.message_user(request, 'Google sheet will be updated')
            return HttpResponseRedirect(request.get_full_path())
        return render(
            request=request,
            template_name='admin/commission/commission_amount.html',
            context={'orders': queryset, 'form': DateRangeForm()}
        )

    report_commission_amount.short_description = 'Report commission amount'  # type: ignore


@admin.register(WorkSphere)
class WorkSphereModelAdmin(admin.ModelAdmin):
    """
    Display table WorkSphere on admin panel
    """

    list_display = ('id', 'name',)


@admin.register(MasterExperience)
class MasterExperienceModelAdmin(admin.ModelAdmin):
    """
    Display table MasterExperience on admin panel
    """

    @staticmethod
    def master_work_sphere(obj: MasterExperience) -> str:
        if obj.work_sphere is not None:
            return obj.work_sphere.name
        return 'Work sphere was remove'

    @staticmethod
    def master_id(obj: MasterExperience) -> str:
        return obj.master.id

    list_display = ('id', 'master_work_sphere', 'experience', 'master_id')
