from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ads.models import Ad, Category, Selection
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "category", "is_published"]


class AdCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field="username",
    )
    category = serializers.SlugRelatedField(
        required=False,
        queryset=Category.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "category", "is_published"]

    def is_valid(self, *, raise_exception=False):
        self._author = get_object_or_404(User, username=self.initial_data.pop('author', []))
        self._category = get_object_or_404(Category, name=self.initial_data.pop('category', []))

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)

        ad.author = self._author
        ad.category = self._category

        ad.save()

        return ad


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        slug_field="username"
    )
    items = AdSerializer(many=True)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Selection
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        request = self.context.get("request")
        self._owner = request.user
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data["owner"] = self._owner
        return super().create(validated_data)

    def save(self, **kwargs):
        selection = super().save()

        selection.owner = self._owner
        selection.save()

        return selection
