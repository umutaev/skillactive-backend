from django.contrib.postgres.fields import ArrayField
from django.db import models

class FeedModel(models.Model):
    class Type(models.TextChoices):
        ARTICLE = "ARTICLE", "Article"
        ARTICLE_SPONSORED = "ARTICLE_SPONSORED", "Sponsored article"
        EVENT = "EVENT", "Event"
        EVENT_SPONSORED = "EVENT_SPONSORED", "Sponsored event"

    title = models.CharField(max_length=1024, blank=False)
    type = models.CharField(max_length=17, choices=Type.choices, blank=False)
    text = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    images = ArrayField(base_field=models.URLField(), size=10)
    date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes_amount = models.IntegerField(default=0)
    views_amount = models.IntegerField(default=0)
    price = models.IntegerField(blank=True, null=True)
