from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(max_length=1024, null=False)
    description = models.TextField(null=True, default=None)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="category_childs",
        on_delete=models.DO_NOTHING,
    )
    deleted = models.BooleanField(default=False)
