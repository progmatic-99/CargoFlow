from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

from shipping.models.voyage import Voyage


class Container(models.Model):
    slug = AutoSlugField(populate_from="container_number", unique=True)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    container_number = models.CharField(max_length=20)
    stuffed = models.BooleanField(default=True)
    destuffed = models.BooleanField(default=False)

    def __str__(self):
        return self.container_number

    def get_absolute_url(self):
        return reverse("container-list")
