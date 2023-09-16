from django.db import models
from django_extensions.db.fields import AutoSlugField


class looseCargo(models.Model):
    slug = AutoSlugField(populate_from="description", unique=True)
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.description} ({self.color})"
