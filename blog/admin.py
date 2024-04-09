from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from blog.models import Category, Comment, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Spanish Translation"), {"fields": ("name_es",)}),
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_on", "last_modified"]
    exclude = ["created_on", "last_modified"]

    fieldsets = (
        (None, {"fields": ("title", "body")}),
        (_("Spanish Translation"), {"fields": ("title_es", "body_es")}),
        ("Other Fields", {"fields": ("categories", "image")}),
    )


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
