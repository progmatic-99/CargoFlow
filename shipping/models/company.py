from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


class Company(models.Model):
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company-list")
