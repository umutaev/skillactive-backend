from rest_framework import serializers
from categories.models import CategoryModel
from feed.models import FeedModel
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db import models


class CategorySerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.parent_category = validated_data.get(
            "parent_category", instance.parent_category
        )
        instance.save()
        return instance

    class Meta:
        model = CategoryModel
        fields = ["id", "name", "description", "parent_category"]
