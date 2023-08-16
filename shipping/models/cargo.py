from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

from .shipper import Shipper
from .consignee import Consignee
from .container import Container


class Cargo(models.Model):
    slug = AutoSlugField(populate_from="weight", unique=True)
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True, blank=True
    )
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.container.container_number})"

    def get_absolute_url(self):
        return reverse("cargo-list")
