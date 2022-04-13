from django.contrib import admin

from api.master.models import Master, MasterExperience, WorkSphere


@admin.register(Master)
class MasterModelAdmin(admin.ModelAdmin):
    """
    Display table Master on admin panel
    """

    # list_display = ('pk', 'user', 'longitude', 'latitude', 'city', 'work_experience')


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
