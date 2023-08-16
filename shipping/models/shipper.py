from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

from .company import Company


class Shipper(models.Model):
    slug = AutoSlugField(populate_from="email", unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

    def get_absolute_url(self):
        return reverse("shipper-list")
