from rest_framework import serializers
from clubs.models import ClubModel


class ClubSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.searchable_title = "".join(
            [
                i.lower()
                for i in validated_data.get("title", instance.title)
                if i.isalpha()
            ]
        )
        instance.address = validated_data.get("address", instance.address)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.min_age = validated_data.get("min_age", instance.min_age)
        instance.max_age = validated_data.get("max_age", instance.max_age)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.opened = validated_data.get("opened", instance.opened)
        instance.images = validated_data.get("images", instance.images)
        instance.save()
        return instance

    class Meta:
        model = ClubModel
        fields = [
            "id",
            "searchable_title",
            "author",
            "title",
            "address",
            "description",
            "price",
            "min_age",
            "max_age",
            "gender",
            "opened",
            "images",
            "comments",
        ]
        extra_kwargs = {
            "comments": {"read_only": True},
        }
