from rest_framework import serializers
from districts.models import DistrictModel


class DistrictSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    class Meta:
        model = DistrictModel
        fields = ["id", "name", "deleted"]
        read_only_fields = ["deleted"]
