from rest_framework import serializers

from .models import Tag, Mail, Client, Message


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
