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
        self._loc = []
        for loc_name in self.initial_data.pop("location", []):
            loc, _ = Location.objects.get_or_create(name=loc_name)
            self._loc.append(loc)

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.location.set(self._loc)
        user.set_password(user.password)

        user.save()
        return user

    def save(self, **kwargs):
        user = super().save()
        user.location.set(self._loc)
        user.set_password(user.password)

        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
