from rest_framework import serializers
from comments.models import CommentModel
from feed.models import FeedModel
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db import models

"""class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    anonymous = serializers.BooleanField(default=False)
    # user = serializers.RelatedField(queryset=get_user_model().objects.all(), required=False)
    user = UserSerializer()
    reply_to = serializers.RelatedField(read_only=True)
    # replies = serializers.RelatedField(many=True, queryset=CommentModel.objects.all())
    feed_item = serializers.PrimaryKeyRelatedField(queryset=FeedModel.objects.all(), required=False)
    # club_item = serializers.PrimaryKeyRelatedField(queryset=ClubModel.objects.all(), required=False)
    name = serializers.CharField(max_length=1024)
    type = serializers.ChoiceField(choices=CommentModel.Type, required=True)
    title = serializers.CharField(max_length=1024)
    rating = serializers.ChoiceField(choices=CommentModel.Rating)
    text = serializers.CharField(required=True)
    images = serializers.ListField()
    creation_date = serializers.DateTimeField(read_only=True)
    likes_amount = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return CommentModel.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.images = validated_data.get('images', instance.images)
        instance.save()
        return instance
    
    class Meta:
        fields = ['id', 'anonymous', 'user', 'reply_to', 'replies', 'feed_item', 'name', 'type', 'title', 'rating', 'text', 'images', 'creation_date', 'likes_amount']
"""

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
