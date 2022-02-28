from rest_framework import serializers
from comments.models import CommentModel
from feed.models import FeedModel
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db import models

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    type = serializers.ChoiceField(choices=CommentModel.Type, required=False)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.images = validated_data.get('images', instance.images)
        instance.save()
        return instance

    class Meta:
        model = CommentModel
        fields = ['id', 'anonymous', 'user', 'reply_to', 'replies', 'feed_item', 'name', 'type', 'title', 'rating', 'text', 'images', 'creation_date', 'likes_amount', 'deleted']
