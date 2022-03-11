from attr import field
from rest_framework import serializers
from clubs.models import ClubModel, PriceObject, TutorObject, CommunicationObject
from comments.serializers import CommentSerializer


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceObject
        fields = ["name", "value"]


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorObject
        fields = ["name", "description", "photo", "phone"]


class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationObject
        fields = ["type", "value"]


class ClubSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        price = validated_data.pop("price")
        tutors = validated_data.pop("tutors")
        contacts = validated_data.pop("contacts")
        price = [PriceObject(**price_item) for price_item in price]
        tutors = [TutorObject(**tutor_item) for tutor_item in tutors]
        contacts = [CommunicationObject(**contact_item) for contact_item in contacts]
        club_instance = ClubModel.objects.create(**validated_data)
        club_instance.price.set(price, bulk=False)
        club_instance.tutors.set(tutors, bulk=False)
        club_instance.contacts.set(contacts, bulk=False)
        club_instance.save()
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
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
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
        if "tutors" in validated_data:
            TutorObject.objects.filter(club=instance).delete()
            tutors = validated_data["tutors"]
            tutors_objects = [
                TutorObject.objects.create(club=instance, **tutor_item)
                for tutor_item in tutors
            ]
            instance.tutors.set(tutors_objects)
        if "contacts" in validated_data:
            CommunicationObject.objects.filter(club=instance).delete()
            contacts = validated_data["contacts"]
            contacts_objects = [
                CommunicationObject.objects.create(club=instance, **contact_item)
                for contact_item in contacts
            ]
            instance.contacts.set(contacts_objects)
        instance.save()
        return instance

    comments = CommentSerializer(read_only=True, many=True)
    price = PriceSerializer(many=True)
    tutors = TutorSerializer(many=True)
    contacts = CommunicationSerializer(many=True)
    free = serializers.BooleanField(read_only=True)

    class Meta:
        model = ClubModel

        fields = [
            "id",
            "searchable_title",
            "author",
            "title",
            "address",
            "latitude",
            "longitude",
            "description",
            "price",
            "min_age",
            "max_age",
            "gender",
            "opened",
            "images",
            "comments",
            "category",
            "free",
            "tutors",
            "contacts",
        ]
        extra_kwargs = {"comments": {"read_only": True}, "free": {"read_only": True}}
