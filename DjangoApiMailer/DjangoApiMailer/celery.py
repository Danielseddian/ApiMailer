import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoApiMailer.settings")

app = Celery("DjangoApiMailer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_mails": {
        "task": "ApiMailer.tasks.send_message",
        "schedule": 300.0,
    }
}
