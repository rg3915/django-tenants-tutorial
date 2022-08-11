from django.contrib import admin

from .models import Customer, Employee


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cpf', 'occupation')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
