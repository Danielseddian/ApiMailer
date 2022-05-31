from celery import shared_task
from .mailers import send_message
from .models import Mail


@shared_task
def send_message():
    message_bodies = Mail.objects.values("text", "messages__client__time_zone", "messages__sent_time").filter(messages__status=False)
    return "Done"
