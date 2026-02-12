from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # to show custom fields in django admin
    list_display = ('email', 'username', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields',
        {'fields': ('user_type', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields',
        {'fields': ('user_type', 'phone_number')}),
    )