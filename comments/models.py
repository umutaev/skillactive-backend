from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.db import models

class CommentModel(models.Model):
    class Type(models.TextChoices):
        COMMENT = "COMMENT", "Comment"
        REVIEW = "REVIEW", "Review"
        ANSWER = "ANSWER", "Answer to review or comment"
    
    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    anonymous = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='replies')  # if answer
    feed_item = models.ForeignKey('feed.FeedModel', null=True, blank=True, on_delete=models.CASCADE, related_name="comments")  # if comment
    club_item = models.ForeignKey('clubs.ClubModel', null=True, blank=True, on_delete=models.CASCADE, related_name="comments")  # if review

    name = models.CharField(max_length=1024, blank=True, null=True)  # if anonymous
    type = models.CharField(max_length=7, choices=Type.choices, blank=False)
    title = models.CharField(max_length=1024, blank=True, null=True)  # if review
    rating = models.IntegerField(choices=Rating.choices, blank=True, null=True)  # if review
    text = models.TextField(blank=False)
    images = ArrayField(base_field=models.URLField(), size=10, blank=True, default=list)
    creation_date = models.DateTimeField(auto_now_add=True)
    likes_amount = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
