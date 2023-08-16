from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

from .company import Company


class ServiceType(models.Model):
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_tonnage = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("service-type-list")
