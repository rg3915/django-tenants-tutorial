from django.apps import apps
from django.contrib import admin
from django_tenants.utils import get_public_schema_name


class TenantsAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    https://stackoverflow.com/a/66898816
    '''

    def has_view_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_add_permission(self, request, view=None):
        return False

    def has_change_permission(self, request, view=None):
        return False

    def has_delete_permission(self, request, view=None):
        return False

    def has_view_or_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e


class CompanyAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    https://stackoverflow.com/a/66898816
    '''
    readonly_fields = ('client',)

    def has_view_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_add_permission(self, request, view=None):
        return False

    def has_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e

    def has_delete_permission(self, request, view=None):
        return False

    def has_view_or_change_permission(self, request, view=None):
        try:
            if request.tenant.schema_name == get_public_schema_name():
                return True
            return False
        except AttributeError:
            return True
        except Exception as e:
            raise e


app = apps.get_app_config('tenant')
for model_name, model in app.models.items():
    admin.site.register(model, TenantsAdmin)

app = apps.get_app_config('company')
for model_name, model in app.models.items():
    admin.site.register(model, CompanyAdmin)
