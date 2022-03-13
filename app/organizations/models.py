from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class OrganizationModel(models.Model):
    name = models.CharField(max_length=1024, null=False)
    owner = models.OneToOneField(
        get_user_model(),
        null=False,
        blank=False,
        primary_key=True,
        on_delete=models.DO_NOTHING,
        related_name="owned_organization",
    )
    managers = models.ManyToManyField(get_user_model(), blank=True)


@receiver(post_save, sender=get_user_model())
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        organization = OrganizationModel(owner=user, name=user.username)
        organization.save()
