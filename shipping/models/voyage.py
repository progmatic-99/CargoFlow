from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from .vessel import Vessel


class Voyage(models.Model):
    slug = AutoSlugField(populate_from="voyage_number", unique=True)
    voyage_number = models.CharField(max_length=50)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    to_port = models.CharField(max_length=200)
    etd = models.DateTimeField(null=True, blank=True)
    grt_nrt = models.FloatField()
    next_port_of_call = models.CharField(max_length=200)
    last_port_of_call = models.CharField(max_length=200)
    master_name = models.CharField(max_length=200)
    eta = models.DateTimeField(null=True, blank=True)
    departed_date = models.DateTimeField(null=True, blank=True)
    etb = models.DateTimeField(null=True, blank=True)
    draft = models.CharField(max_length=200)
    ship_length = models.PositiveIntegerField()
    ship_breadth = models.PositiveIntegerField()
    vessel_on_port = models.BooleanField(default=True)
    vessel_on_anchorage = models.BooleanField(default=True)

    # def __str__(self):
    #     return f"({self.voyage_number}) - {self.from_port} -> {self.to_port}"

    def get_absolute_url(self):
        return reverse("voyage-list")
