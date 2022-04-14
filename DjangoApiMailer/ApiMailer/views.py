from rest_framework.viewsets import ModelViewSet
from datetime import datetime as dt

from .serializers import Client, ClientSerializer, Mail, MailSerializer, Message, MessageSerializer

BASE_UTC = 3


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        request.data["UTC"] = (data := request.data).get("UTC") or data.get("utc") or data.get("time_zone") or BASE_UTC
        request.data["phone"] = int(data.get("phone")) or int(data.get("mobile"))
        request.data["phone_code"] = int(data.get("phone_code")) or int(str(data["phone"])[1:4])
        super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(tags=self.request.data["tags"])

    def perform_update(self, serializer):
        serializer.save(tags=self.request.data["tags"])


class MailViewSet(ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    def perform_create(self, serializer):
        serializer.save(clients=self.request.data.get("clients"))
        for client in (data := serializer.data).get("clients"):
            MessageSerializer(mailing=data["id"], client=client["id"], sent_time=dt.now(), status=False).save()
