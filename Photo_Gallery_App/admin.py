from django.contrib import admin
from .models import Profile, Photo, Tag, Like
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_by", "upload_date")
    search_fields = ("title", "description")
    list_filter = ("upload_date", "tags")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "photo", "value", "created_at")
    list_filter = ("value",)