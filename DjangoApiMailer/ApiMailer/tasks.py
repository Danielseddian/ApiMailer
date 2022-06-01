from celery import shared_task
from django.db.models import F
from datetime import timedelta as td, datetime as dt, timezone as tz

from .mailers import send_message
from .models import Message


@shared_task
def send_message():
    messages = Message.objects.values(
        "id",
        text=F("mailing__text"),
        start=F("mailing__start"),
        end=F("mailing__end"),
        phone=F("clients__phone"),
        zone=F("clients__time_zone"),
    ).filter(status=False)
    for message in messages:
        zone = td(hours=message.pop("zone"))
        if message.pop("start") + zone < dt.now(tz(zone)) < message.pop("end") + zone:
            if (response := send_message(message)).status_code == 200:
                Message.objects.get(id=message["id"])
            else:
                return response
    return "Done"
