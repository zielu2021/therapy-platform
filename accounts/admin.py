from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "is_active",
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)
