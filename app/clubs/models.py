from email.mime import base
from email.policy import default
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from categories.models import CategoryModel
from districts.models import DistrictModel


class PriceObject(models.Model):
    name = models.CharField(max_length=1024)
    value = models.IntegerField()
    club = models.ForeignKey(
        "clubs.ClubModel", related_name="price", on_delete=models.CASCADE
    )


class TutorObject(models.Model):
    name = models.CharField(max_length=1024, null=False)
    photo = models.URLField(null=True)
    description = models.TextField(null=True)
    phone = models.CharField(max_length=256, null=True)
    club = models.ForeignKey(
        "clubs.ClubModel", related_name="tutors", on_delete=models.CASCADE
    )


class CommunicationObject(models.Model):
    class Type(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        PHONE = "PHONE", "Phone"
        SITE = "SITE", "Website"
        VK = "VK", "Vkontakte"
        INSTAGRAM = "INSTAGRAM", "Instagram"
        OTHER = "OTHER", "Others"

    type = models.CharField(choices=Type.choices, max_length=9, null=False)
    value = models.CharField(max_length=256)
    club = models.ForeignKey(
        "clubs.ClubModel", related_name="contacts", on_delete=models.CASCADE
    )


class TimetableObject(models.Model):
    class DayOfTheWeek(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    day_of_the_week = models.IntegerField(choices=DayOfTheWeek.choices)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    club = models.ForeignKey(
        "clubs.ClubModel", related_name="timetable", on_delete=models.CASCADE
    )


class ClubModel(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        BOTH = "BOTH", "Male and Female"

    author = models.ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="clubs",
    )
    title = models.CharField(max_length=1024, null=False)
    searchable_title = models.CharField(max_length=1024, null=False)
    address = models.CharField(max_length=1024, null=False)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    description = models.TextField()
    # timetable
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(
        choices=Gender.choices, max_length=6, default=Gender.BOTH, null=False
    )
    opened = models.BooleanField(default=True, null=False)
    category = models.ForeignKey(
        CategoryModel, null=True, blank=False, on_delete=models.DO_NOTHING
    )
    district = models.ForeignKey(
        DistrictModel, null=True, blank=False, on_delete=models.DO_NOTHING
    )
    images = ArrayField(base_field=models.URLField(), size=10, blank=True, default=list)
    free = models.BooleanField(default=False)
    public = models.BooleanField(default=False)


@receiver(post_save, sender=ClubModel)
def free_field_callback(sender, instance, *args, **kwargs):
    paid = PriceObject.objects.filter(club=instance, value__gt=0).count()
    instance.free = not bool(paid)
