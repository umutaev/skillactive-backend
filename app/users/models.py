from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    owner = models.OneToOneField(
        get_user_model(),
        null=False,
        blank=False,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    profile_photo = models.CharField(max_length=1024, null=True, default=None)
    blocked = models.BooleanField(default=False)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(owner=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
