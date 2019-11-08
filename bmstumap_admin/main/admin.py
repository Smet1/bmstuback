from django.contrib import admin
from main.models import (
    Cabinet, Position, Employee, Schedule, PosHeld, Floor, Degree
)
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from main.forms import ScheduleAdminForm


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    class Meta:
        js = (
            'main/map.js',
        )

    list_display = ('floor', 'name', 'latitude', 'longitude')
    fields = (
        'floor',
        'name',
        'longitude',
        'latitude',
        'auditoria',
        'node',
        'map'
    )

    list_filter = ('auditoria', )
    readonly_fields = ('map',)
    def map(self, obj):
        template = get_template('bmstuplan.svg')
        if obj.pk:
            all_markers = Cabinet.objects.exclude(pk__in=[obj.pk])
        else:
            all_markers = Cabinet.objects.all()
        return mark_safe(template.render({'markers': all_markers}))


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name')
    fields = (
        'last_name',
        'first_name',
        'middle_name',
        'degree',
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm

    list_display = ('employee', 'cabinet', 'time_from', 'time_to', 'weekday', 'week_type')


@admin.register(PosHeld)
class PosHeldAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position' )
