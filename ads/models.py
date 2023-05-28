from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="Название"
        verbose_name_plural = "Названия"


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=200)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='logos/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="Имя"
        verbose_name_plural = "Имена"
