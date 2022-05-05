from django.contrib import admin

from .models import Task, Solution


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    shown_fields = ["name", "text", "task", "code", "expected", "is_pub"]
    list_display = ["id"] + shown_fields
    list_editable = shown_fields
    list_filter = shown_fields


@admin.register(Solution)
class TaskAdmin(admin.ModelAdmin):
    shown_fields = ["id", "user", "task", "input"]
    list_display = shown_fields
    list_filter = shown_fields
