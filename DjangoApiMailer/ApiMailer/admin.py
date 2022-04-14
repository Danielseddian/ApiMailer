from django.contrib import admin

from .models import Client, Mail, Message, Tag


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    shown_fields = ("id", "phone", "utc")
    list_display = shown_fields
    list_editable = ("utc",)
    filter_horizontal = ("tags", )
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    shown_fields = ["id", "start", "end", "text"]
    list_display = shown_fields
    list_editable = ["text"]
    # list_display_links = ()
    # filter_horizontal = ()
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Message)
class MesageAdmin(admin.ModelAdmin):
    shown_fields = ["client", "mailing"]
    list_display = shown_fields + ["id"]
    # list_editable = ()
    # list_display_links = ()
    # filter_horizontal = ()
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # list_editable = ()
    # list_display_links = ()
    # filter_horizontal = ()
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"

