import asyncio

from rest_framework import serializers
from datetime import datetime as dt, timezone as tz, timedelta as td

from DjangoApiMailer.settings import MAILING_URL
from .mailers import send_mailing_by_url
from .models import Tag, Mail, Client, Message
from .validators import validate_phone_length

BASE_UTC = 3


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tag


class ClientSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Client

    def validate_phone(self, phone):
        validate_phone_length(phone)
        return super().validate(phone)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Message


class MailSerializer(serializers.ModelSerializer):
    KEYS = {
        "ids": "id__in",
        "phones": "phone__in",
        "tags": "tags__in",
        "utc": "utc__in",
        "phone_codes": "phone_code__in",
    }
    clients = ClientSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Mail

    def create(self, data):
        clients = Client.objects.filter(**self.get_filters(data.pop("clients")))
        mailing = Mail.objects.create(**data)
        mailing.clients.set(clients)
        self.create_messages(mailing, clients)
        return mailing

    def update(self, mailing, data):
        clients = Client.objects.filter(**self.get_filters(data.pop("clients")))
        self.make_new_messages(mailing, clients)
        mailing.clients.set(clients)
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
