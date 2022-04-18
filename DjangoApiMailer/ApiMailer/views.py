from rest_framework.viewsets import ModelViewSet

from .serializers import Client, ClientSerializer, Mail, MailSerializer, BASE_UTC


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        data["utc"] = (data := request.data).get("utc") or data.get("UTC") or data.get("time_zone") or BASE_UTC
        data["phone"] = data.get("phone") or data.get("mobile")
        data["phone_code"] = data.get("phone_code") or int(str(data["phone"])[1:4])
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(tags=self.request.data["tags"])

    def perform_update(self, serializer):
        serializer.save(tags=self.request.data["tags"])


class MailViewSet(ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    clients = Client.objects.all().only("id")

    def perform_create(self, serializer):
        serializer.save(clients=self.request.data.get("clients", []))
