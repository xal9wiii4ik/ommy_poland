from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from api.master.models import Master, MasterExperience, WorkSphere


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


@admin.register(WorkSphere)
class WorkSphereModelAdmin(admin.ModelAdmin):
    """
    Display table WorkSphere on admin panel
    """


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
