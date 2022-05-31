from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    task = models.TextField()
    code = models.TextField()
    call = models.CharField(max_length=300)
    data = ArrayField(models.IntegerField())

    is_pub = models.BooleanField(default=True)


class Solution(models.Model):
    folder = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="responses")
    date = models.DateTimeField(auto_now=True)
    resolve = models.TextField(blank=True, null=True)
