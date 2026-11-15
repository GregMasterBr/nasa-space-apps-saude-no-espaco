
from django.contrib import admin
from .models import (
    Astronaut,
    Mission,
    MissionAssignment,
    ResearchSubject,
    HealthRecord
)


@admin.register(Astronaut)
class AstronautAdmin(admin.ModelAdmin):
    list_display = ('full_name','occupation','agency', 'nationality')
    search_fields = ('full_name', 'nationality')
    list_filter = ('agency', 'nationality')


class MissionAssignmentInline(admin.TabularInline):
    model = MissionAssignment
    extra = 1


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'launch_date', 'status')
    list_filter = ('agency', 'status')
    search_fields = ('name',)
    inlines = [MissionAssignmentInline]


@admin.register(MissionAssignment)
class MissionAssignmentAdmin(admin.ModelAdmin):
    list_display = ('astronaut', 'mission', 'role', 'crew_type')
    list_filter = ('mission', 'crew_type')


@admin.register(ResearchSubject)
class ResearchSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'mission')
    list_filter = ('mission',)
    search_fields = ('subject_code',)
@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):

    list_display = (
        'subject',
        'study_code',
        'parameter',
        'value',
        'unit',
        'reference_min',
        'reference_max',
        'timepoint',
        'sample_type',
        'sex',
        'test_type',
    )

    list_filter = (
        'study_code',
        'parameter',
        'timepoint',
        'sex',
        'test_type',
    )

    search_fields = (
        'subject__subject_code',
        'parameter',
        'study_code',
    )

    ordering = (
        'subject__subject_code',
        'timepoint',
        'parameter',
    )