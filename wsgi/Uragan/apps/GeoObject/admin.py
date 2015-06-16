from django.contrib import admin

from .models import GeoObject, Images, SurveillancePlan
# Register your models here.

admin.site.register(GeoObject, admin.ModelAdmin)
admin.site.register(SurveillancePlan, admin.ModelAdmin)
admin.site.register(Images, admin.ModelAdmin)