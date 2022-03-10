from rest_framework import serializers
from clubs.models import ClubModel, PriceObject
from comments.serializers import CommentSerializer


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceObject
        fields = ["name", "value"]


class ClubSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        price = validated_data.pop("price")
        club_instance = ClubModel.objects.create(**validated_data)
        for price_item in price:
            PriceObject.objects.create(club=club_instance, **price_item)
        return club_instance

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
        instance.min_age = validated_data.get("min_age", instance.min_age)
        instance.max_age = validated_data.get("max_age", instance.max_age)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.opened = validated_data.get("opened", instance.opened)
        instance.images = validated_data.get("images", instance.images)
        instance.category = validated_data.get("category", instance.category)
        if "price" in validated_data:
            PriceObject.objects.filter(club=instance).delete()
            price = validated_data["price"]
            price_objects = [
                PriceObject.objects.create(club=instance, **price_item)
                for price_item in price
            ]
            instance.price.set(price_objects)
        instance.save()
        return instance

    comments = CommentSerializer(read_only=True, many=True)
    price = PriceSerializer(many=True)

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
            "category",
        ]
        extra_kwargs = {
            "comments": {"read_only": True},
        }
