from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from .vessel import Vessel


class Voyage(models.Model):
    slug = AutoSlugField(populate_from="voyage_number", unique=True)
    voyage_number = models.CharField(max_length=50)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    to_port = models.CharField(max_length=200)
    grt = models.FloatField()
    nrt = models.FloatField()
    next_port_of_call = models.CharField(max_length=200)
    last_port_of_call = models.CharField(max_length=200)
    master_name = models.CharField(max_length=200)
    eta = models.DateTimeField(null=True, blank=True)
    etb = models.DateTimeField(null=True, blank=True)
    etd = models.DateTimeField(null=True, blank=True)
    departed_date = models.DateTimeField(null=True, blank=True)
    draft = models.CharField(max_length=200)
    vessel_on_port = models.BooleanField(default=True)
    vessel_on_anchorage = models.BooleanField(default=True)
    owner = models.CharField(max_length=200)
    pi_club = models.CharField(max_length=200)
    purpose_of_call = models.CharField(max_length=500, null=True, blank=True)
    import_no = models.CharField(max_length=15, null=True, blank=True)
    export_no = models.CharField(max_length=15, null=True, blank=True)
    cha_boe = models.TextField(null=True, blank=True)
    agent_importer = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"({self.vessel.name}) : ({self.voyage_number}) - {self.last_port_of_call} -> {self.to_port}"

    def get_absolute_url(self):
        return reverse("voyage-list")
