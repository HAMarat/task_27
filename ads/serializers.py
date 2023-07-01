from rest_framework import serializers

from ads.models import Ad, Category, Selection
from users.models import User


class IsNotTrueValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("Объявление нельзя сразу опубликовать")


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "category", "is_published"]


class AdCreateSerializer(serializers.ModelSerializer):
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
    is_published = serializers.BooleanField(
        validators=[IsNotTrueValidator()]
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "category", "is_published"]


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
