from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
