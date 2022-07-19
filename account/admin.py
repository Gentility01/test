from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Acount
# Register your models here.


# note: when you try to login to the admin there will be no user so we need to CUSTOMIZE our django  so that it will understand what it should do with our admin
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets  = ()


admin.site.register(Acount, AccountAdmin)
