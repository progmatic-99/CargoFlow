from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


class Vendor(models.Model):
    slug = AutoSlugField(populate_from="contact_person", unique=True)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    account_no = models.CharField(max_length=15)
    ifsc_code = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

    def get_absolute_url(self):
        return reverse("vendor-list")
