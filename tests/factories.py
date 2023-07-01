import factory.django

from ads.models import Ad, Category
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "test_password"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("slug")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")
    author = factory.SubFactory(UserFactory)
    price = 650
    is_published = False
