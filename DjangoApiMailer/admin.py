from django.contrib import admin

from .models import Client, Mail, Message, Tag


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    shown_fields = ("id", "phone", "utc")
    list_display = shown_fields
    list_display_links = ("id", "phone",)
    list_editable = ("time_zone",)
    filter_horizontal = ("tags", )
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    shown_fields = ["id", "start", "end", "text"]
    list_display = shown_fields
    list_editable = ["text"]
    list_display_links = ("id", "start",)
    filter_horizontal = ("clients",)
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Message)
class MesageAdmin(admin.ModelAdmin):
    shown_fields = ["id", "client", "mailing"]
    list_display = shown_fields
    list_display_links = shown_fields
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    shown_fields = ["name", "slug"]
    list_display = ["id"] + shown_fields
    list_editable = shown_fields
    search_fields = ("name", "slug")
    list_filter = ("name", "slug")
    empty_value_display = "-пусто-"

