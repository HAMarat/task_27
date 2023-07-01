from rest_framework import serializers

from users.models import User, Location


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)

        user.save()
        return user

    def save(self, **kwargs):
        user = super().save()
        user.set_password(user.password)

        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
