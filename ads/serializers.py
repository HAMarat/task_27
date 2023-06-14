from rest_framework import serializers

from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price"]
