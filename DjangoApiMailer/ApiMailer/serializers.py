from rest_framework import serializers
from datetime import datetime as dt, timezone as tz, timedelta as td

from .models import Tag, Mail, Client, Message

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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Message


class MailSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Mail

    def create(self, data):
        filters = {
            "id__in" if key == "ids" else key + "__in": value
            for key, value in data.pop("clients").items()
            if key in ("ids", "tags", "utc")
        }
        mailing = Mail.objects.create(**data)
        mailing.clients.set(Client.objects.filter(**filters))
        self.create_messages(mailing)
        return mailing

    @staticmethod
    def create_messages(mailing):
        messages = [
            Message(sent_time=dt.now(tz(td(hours=BASE_UTC))), status=False, mailing=mailing, client=client)
            for client in mailing.clients.filter()
        ]
        Message.objects.bulk_create(messages)
