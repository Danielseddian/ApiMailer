from transliterate import translit
from rest_framework import serializers
from datetime import datetime as dt, timezone as tz, timedelta as td
from django.utils.text import slugify

from .models import Tag, Mail, Client, Message
from .validators import validate_phone

BASE_UTC = 3


def translit_ru_en(text):
    return translit(text, "ru", reversed=True)


def bulk_get_or_create_tags(tags):
    return [Tag.objects.get_or_create(name=tag, slug=slugify(translit_ru_en(tag)))[0] for tag in tags]


class ClientSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField("name", read_only=True, many=True)

    class Meta:
        fields = "__all__"
        model = Client

    def validate_phone(self, phone):
        validate_phone(phone)
        return super().validate(phone)


class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        fields = "__all__"
        model = Message


class MailSerializer(serializers.ModelSerializer):
    KEYS = {
        "ids": "id__in",
        "phones": "phone__in",
        "tags": "tags__name__in",
        "time_zones": "time_zone__in",
        "phone_codes": "phone_code__in",
    }
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Mail

    def create(self, data):
        clients = Client.objects.filter(**self.get_filters(data.pop("clients")))
        mailing = Mail.objects.create(**data)
        self.create_messages(mailing, clients)
        return mailing

    def update(self, mailing, data):
        clients = Client.objects.filter(**self.get_filters(data.pop("clients")))
        self.make_new_messages(mailing, clients)
        super().update(mailing, data)
        return mailing

    def get_filters(self, data) -> dict:
        return {self.KEYS[key]: value for key, value in data.items() if key in self.KEYS}

    def make_new_messages(self, mailing, clients):
        self.create_messages(
            mailing,
            clients.exclude(id__in=(message.client.id for message in Message.objects.filter(mailing__id=mailing.id))),
        )

    @staticmethod
    def create_messages(mailing, clients):
        message_bodies = [
            Message(sent_time=dt.now(tz(td(hours=BASE_UTC))), status=False, mailing=mailing, client=client)
            for client in clients
        ]
        Message.objects.bulk_create(message_bodies)
