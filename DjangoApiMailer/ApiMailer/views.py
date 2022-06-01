from rest_framework.viewsets import ModelViewSet
from django.utils.text import slugify

from .serializers import Client, ClientSerializer, Mail, MailSerializer, BASE_UTC, bulk_get_or_create_tags


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        data["phone"] = (str((data := request.data).get("phone") or str(data.get("mobile")))).replace("+", "")
        data["phone_code"] = data.get("phone_code") or data.get("mobile_code") or data["phone"][1:4]
        data["time_zone"] = data.get("utc") or data.get("UTC") or data.get("time_zone") or BASE_UTC
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(tags=bulk_get_or_create_tags(self.request.data.get("tags", [])))

    def perform_update(self, serializer):
        tags = bulk_get_or_create_tags(self.request.data.get("tags", []))
        serializer.save(tags=bulk_get_or_create_tags(self.request.data.get("tags", [])))


class MailViewSet(ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    def perform_create(self, serializer):
        serializer.save(clients=self.request.data.get("clients", []))

    def perform_update(self, serializer):
        serializer.save(clients=self.request.data.get("clients", []))
