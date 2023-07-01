from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=10, unique=True, validators=[MinValueValidator(5)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="Название"
        verbose_name_plural = "Названия"


class Ad(models.Model):
    name = models.CharField(max_length=200, null=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(null=True)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='logos/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="Имя"
        verbose_name_plural = "Имена"


class Selection(models.Model):
    items = models.ManyToManyField(Ad)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="Подборка"
        verbose_name_plural = "Подборки"
