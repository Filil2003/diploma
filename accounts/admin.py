from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_display = ('email', 'is_staff', 'is_superuser', 'last_login', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'created_at', 'last_login')
    fieldsets = (
        (
            None,
            {
                'fields': ('email',)
            }
        ),
        (
            _('Permissions'),
            {
                'classes': ('collapse',),
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login', 'created_at'),
            }
        )
    )
    readonly_fields = ('last_login', 'created_at',)
