# coding: utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import TLE, Satellite, SubsatellitePoint
# Register your models here.

class TLE_Admin(admin.ModelAdmin):
    readonly_fields = 'datetime_in_lines', 'satellite', 'datetime_created',
    list_display = 'title_line', 'datetime_in_lines', 'datetime_created',
    date_hierarchy = 'datetime_in_lines'
    list_filter = 'satellite', 'title_line'
    fieldsets = (
        ('TLE', {'fields': ('title_line', 'line1', 'line2')}),
        (_('Autocomplete'), {'fields': ('datetime_in_lines', 'satellite')}),
    )
    exclude = 'datetime_created',


class TLE_StackedInline(admin.StackedInline):
    model = TLE


class SatelliteAdmin(admin.ModelAdmin):
    inlines = [
        TLE_StackedInline,
    ]


class SubsatellitePoint_Admin(admin.ModelAdmin):
    readonly_fields = 'date_time', 'location', 'tle',
    list_display = 'date_time', 'location', 'tle',
    date_hierarchy = 'date_time'
    list_filter = 'tle',


admin.site.register(TLE, TLE_Admin)
admin.site.register(Satellite, admin.ModelAdmin)
admin.site.register(SubsatellitePoint, SubsatellitePoint_Admin)
