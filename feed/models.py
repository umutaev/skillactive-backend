from django.contrib.postgres.fields import ArrayField
from django.db import models

class FeedModel(models.Model):
    class Type(models.TextChoices):
        ARTICLE = "AR", "Article"
        ARTICLE_SPONSORED = "AS", "Sponsored article"
        EVENT = "EV", "Event"
        EVENT_SPONSORED = "ES", "Sponsored event"

    title = models.CharField(max_length=1024, blank=False)
    type = models.CharField(max_length=2, choices=Type.choices, blank=False)
    text = models.TextField(blank=True)
    address = models.CharField(max_length=1024, blank=True)
    images = ArrayField(base_field=models.URLField(), size=10)
    date = models.DateTimeField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes_amount = models.IntegerField(default=0)
    views_amount = models.IntegerField(default=0)
    price = models.IntegerField(blank=True)
