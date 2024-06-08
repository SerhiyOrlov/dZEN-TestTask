from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'homepage',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'display_homepage',)

    def display_homepage(self, obj):
        return obj.homepage

    display_homepage.short_description = 'Homepage'


admin.site.register(User, CustomUserAdmin)


