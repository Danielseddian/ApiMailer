from rest_framework.viewsets import ModelViewSet

from .serializers import Client, ClientSerializer, Mail, MailSerializer, BASE_UTC


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        data["phone"] = str((data := request.data).get("phone") or data.get("mobile")).replace("+", "")
        data["phone_code"] = data.get("phone_code") or data.get("mobile_code") or data["phone"][1:4]
        data["utc"] = data.get("utc") or data.get("UTC") or data.get("time_zone") or BASE_UTC
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(tags=self.request.data.get("tags", []))

    def perform_update(self, serializer):
        serializer.save(tags=self.request.data.get("tags", []))


class MailViewSet(ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    def perform_create(self, serializer):
        serializer.save(clients=self.request.data.get("clients", []))

    def perform_update(self, serializer):
        serializer.save(clients=self.request.data.get("clients", []))
