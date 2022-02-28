from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model


class ClubModel(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        BOTH = "BOTH", "Male and Female"

    author = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, null=False)
    searchable_title = models.CharField(max_length=1024, null=False)
    address = models.CharField(max_length=1024, null=False)
    description = models.TextField()
    # contacts
    # tutors
    # timetable
    price = models.IntegerField(default=0, null=False)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(choices=Gender.choices, max_length=6, default=Gender.BOTH, null=False)
    opened = models.BooleanField(default=True, null=False)
    # tags
    # category, from model
    images = ArrayField(base_field=models.URLField(), size=10, blank=True, default=list)
