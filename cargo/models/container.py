from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


CONTAINER_STATUS = [(1, "EMPTY"), (2, "STUFF")]


class Container(models.Model):
    slug = AutoSlugField(populate_from="container_number", unique=True)
    container_number = models.CharField(max_length=20)
    container_status = models.CharField(max_length=10, choices=CONTAINER_STATUS)
    tare_weight = models.FloatField()
    on_port = models.BooleanField(default=False)  # Change this line

    def __str__(self):
        return self.container_number

    def get_absolute_url(self):
        return reverse("container-list")
