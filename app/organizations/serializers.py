from rest_framework import serializers
from organizations.models import OrganizationModel
from django.contrib.auth import get_user_model


class OrganizationSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        if "managers" in validated_data:
            managers = validated_data["managers"]
            print(managers)
            instance.managers.set(managers)
        instance.save()
        return instance

    class Meta:
        model = OrganizationModel
        fields = ["name", "owner", "managers"]
        extra_kwargs = {"owner": {"read_only": True}}
