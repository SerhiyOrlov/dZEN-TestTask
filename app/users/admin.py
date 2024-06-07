from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Определите отображаемые поля пользователя
    fieldsets = (
        (None, {'fields': ('username', 'email', 'homepage',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'homepage')


admin.site.register(User, CustomUserAdmin)
