from django.core import validators
from django.db import models

MIN = validators.MinValueValidator
MAX = validators.MaxValueValidator
STATUS = {True: "доставлено", False: "не доставлено"}


class Tag(models.Model):
    name = models.CharField(verbose_name="Имя тега", max_length=100, unique=True)
    slug = models.SlugField(verbose_name="slug", max_length=20, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("slug",)

    def __str__(self):
        return f"Id: {self.id}, название: {self.name}, метка: {self.slug}"


class Client(models.Model):
    phone = models.PositiveIntegerField(verbose_name="Номер телефона", unique=True)
    phone_code = models.PositiveSmallIntegerField(verbose_name="Код мобильного оператора")
    tags = models.ManyToManyField(Tag, verbose_name="Тег", related_name="clients")
    time_zone = models.SmallIntegerField(validators=[MIN(-12), MAX(12)])

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("phone",)

    def __str__(self):
        return f"Id: {self.id}, телефон: {self.phone}, код оператора: {self.phone_code} часовой пояс: {self.time_zone}"


class Mail(models.Model):
    start = models.DateTimeField(verbose_name="Дата и время начала рассылки", null=True, blank=True)
    text = models.TextField(verbose_name="Текст сообщения")
    clients = models.ManyToManyField(Client, verbose_name="Получатели", related_name="mails")
    end = models.DateTimeField(verbose_name="Дата и время окончания рассылки", null=True, blank=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("start",)

    def __str__(self):
        return f"id: {self.id}, текст сообщения: {self.text[:50]}, начало рассылки: {self.start}, окочание: {self.end}"


class Message(models.Model):
    status = models.BooleanField(verbose_name="Статус отправки")
    sent_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата отправки")
    mailing = models.ForeignKey(Mail, verbose_name="Рассылка", on_delete=models.CASCADE, related_name="messages")
    client = models.ForeignKey(Client, verbose_name="Кому", on_delete=models.CASCADE, related_name="messages")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("sent_time",)
        constraints = [
            models.UniqueConstraint(
                fields=["mailing", "client"],
                name="uniq_mail",
            ),
        ]

    def __str__(self):
        return (
            f"Id: {self.id}, сообщение: {self.mailing.text[:25]} клиенту: id: {self.client.id}, телефон: "
            f"**{str(self.client.phone)[-4:]}, отправлено:  {self.sent_time}, статус: {STATUS[self.status]}"
        )
