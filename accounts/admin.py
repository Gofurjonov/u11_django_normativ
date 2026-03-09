from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Userni ichida profiIni ko'rsatish"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


# Userni qayta registratsiya qilish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview']

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" style="border-radius:50%"/>'
        return "Rasm yo'q"

    avatar_preview.allow_tags = True
    avatar_preview.short_description = "Profil rasmi"