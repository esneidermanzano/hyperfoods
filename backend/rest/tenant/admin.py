from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from tenant.models import Tenant

@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'paid_until')