
from django.contrib import admin

from .models import (
    Astronaut,
    Mission,
    MissionAssignment,
    ResearchSubject,
    HealthRecord,
    FamilyContact,
    CommunicationCall,
    CommunicationChecklist,
    CommunicationChecklistItem,
)


@admin.register(Astronaut)
class AstronautAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'occupation', 'agency', 'nationality')
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
        'subject', 'study_code', 'parameter', 'value',
        'unit', 'reference_min', 'reference_max',
        'timepoint', 'sample_type', 'sex', 'test_type',
    )

    list_filter = (
        'study_code', 'parameter', 'timepoint', 'sex', 'test_type',
    )

    search_fields = (
        'subject__subject_code', 'parameter', 'study_code',
    )

    ordering = (
        'subject__subject_code', 'timepoint', 'parameter',
    )


@admin.register(FamilyContact)
class FamilyContactAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'astronaut', 'relationship', 'is_primary', 'is_active',
    )
    list_filter = ('is_primary', 'is_active')
    search_fields = ('name', 'astronaut__full_name')


@admin.register(CommunicationCall)
class CommunicationCallAdmin(admin.ModelAdmin):
    list_display = (
        'astronaut', 'contact', 'status',
        'scheduled_at', 'started_at', 'ended_at',
    )
    list_filter = ('status',)
    search_fields = ('astronaut__full_name', 'contact__name')


class CommunicationChecklistItemInline(admin.TabularInline):
    model = CommunicationChecklistItem
    extra = 1


@admin.register(CommunicationChecklist)
class CommunicationChecklistAdmin(admin.ModelAdmin):
    list_display = (
        'astronaut', 'checklist_type', 'status',
        'completed_at', 'created_at',
    )
    list_filter = ('checklist_type', 'status')
    search_fields = ('astronaut__full_name',)
    inlines = [CommunicationChecklistItemInline]
