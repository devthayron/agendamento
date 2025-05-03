# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['username', 'email', 'is_staff', 'is_active', 'is_gerente']
    list_filter = ['is_staff', 'is_active', 'is_gerente']
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_gerente',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_gerente',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
