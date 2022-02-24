from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from core.models import Preference


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')


admin.site.register(Preference, PreferenceAdmin)

admin.site.register(Account, AccountAdmin)
