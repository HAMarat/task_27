import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from rest_framework.exceptions import ValidationError


def check_birth_date(value: datetime.date):
    if relativedelta(datetime.date.today(), value).years < 9:
        raise ValidationError("Возраст менее 9 лет")


def check_email(value: str):
    if "@rambler.ru" in value:
        raise ValidationError("Недопустимый почтовый адрес")


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название"
        verbose_name_plural = "Названия"


class UserRole(TextChoices):
    MEMBER = "member", "Пользователь"
    MODERATOR = "moderator", "Модератор"
    ADMIN = "admin", "Администратор"


class User(AbstractUser):
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    username = models.CharField(max_length=40, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=40, choices=UserRole.choices, default=UserRole.MEMBER)
    age = models.SmallIntegerField(null=True)
    location = models.ManyToManyField(Location, null=True)
    birt_date = models.DateField(null=True, validators=[check_birth_date])
    email = models.EmailField(null=True, unique=True, validators=[check_email])

    # def __str__(self):
    #     return self.username

    class Meta:
        verbose_name = "Имя пользователя"
        verbose_name_plural = "Имена пользователей"
