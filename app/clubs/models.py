from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
from categories.models import CategoryModel


class PriceObject(models.Model):
    name = models.CharField(max_length=1024)
    value = models.IntegerField()
    club = models.ForeignKey(
        "clubs.ClubModel", related_name="price", on_delete=models.CASCADE
    )


class ClubModel(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        BOTH = "BOTH", "Male and Female"

    author = models.ForeignKey(
        get_user_model(), null=False, blank=False, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=1024, null=False)
    searchable_title = models.CharField(max_length=1024, null=False)
    address = models.CharField(max_length=1024, null=False)
    description = models.TextField()
    # contacts
    # tutors
    # timetable
    # price = models.IntegerField(default=0, null=False)
    # price = ArrayField(base_field=PriceObject, blank=True, default=list)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(
        choices=Gender.choices, max_length=6, default=Gender.BOTH, null=False
    )
    opened = models.BooleanField(default=True, null=False)
    # tags
    category = models.ForeignKey(
        CategoryModel, null=True, blank=False, on_delete=models.DO_NOTHING
    )
    images = ArrayField(base_field=models.URLField(), size=10, blank=True, default=list)
