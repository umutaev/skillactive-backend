from django.db import models


class ApplicationModel(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        PROCESSING = "PROCESSING", "Application in progress"
        SEEN = "SEEN", "Application seen"

    club = models.ForeignKey(
        "clubs.ClubModel",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(choices=Status.choices, max_length=10, default=Status.NEW)
    name = models.CharField(max_length=1024, null=False)
    phone = models.CharField(max_length=64, null=False)
    text = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
