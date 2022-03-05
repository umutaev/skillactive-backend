from rest_framework import serializers
from feed.models import FeedModel
from comments.serializers import CommentSerializer
from django.db import models


class FeedSerialier(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=1024)
    type = serializers.ChoiceField(choices=FeedModel.Type, required=True)
    text = serializers.CharField(required=False)
    address = serializers.CharField(max_length=1024, required=False, allow_null=True)
    images = serializers.ListField(required=True)
    date = serializers.DateTimeField(required=False, allow_null=True)
    creation_date = serializers.DateTimeField(read_only=True)
    likes_amount = serializers.IntegerField(read_only=True)
    views_amount = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(required=False, allow_null=True)
    comments = CommentSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return FeedModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.type = validated_data.get("type", instance.type)
        instance.text = validated_data.get("text", instance.text)
        instance.address = validated_data.get("address", instance.address)
        instance.images = validated_data.get("images", instance.images)
        instance.date = validated_data.get("date", instance.date)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance
