from django.contrib import admin

from core.models import Doctor, State


class DoctorAdmin(admin.ModelAdmin):
    pass


class StateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(State, StateAdmin)
