from django.db import models


class DistrictModel(models.Model):
    name = models.CharField(max_length=1024, null=False)
    deleted = models.BooleanField(default=False)
