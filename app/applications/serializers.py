from rest_framework import serializers
from applications.models import ApplicationModel


class ApplicationSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = ApplicationModel
        fields = ["id", "status", "club", "name", "phone", "text", "creation_date"]
        extra_kwargs = {"creation_date": {"read_only": True}}
