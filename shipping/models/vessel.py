from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


class Vessel(models.Model):
    slug = AutoSlugField(populate_from="imo_number", unique=True)
    name = models.CharField(max_length=200)
    imo_number = models.CharField(max_length=15)
    flag = models.CharField(max_length=50)
    call_sign = models.CharField(max_length=200)
    official_no = models.IntegerField()
    registry_port = models.CharField(max_length=200)
    mmsi = models.FloatField()
    loa = models.FloatField()
    beam = models.FloatField()
    depth = models.FloatField()
    owner = models.CharField(max_length=200)
    pi_club = models.CharField(max_length=200)
    charter_type = models.CharField(max_length=200)
    purpose_of_call = models.CharField(max_length=500, null=True, blank=True)
    import_no = models.CharField(max_length=15, null=True, blank=True)
    export_no = models.CharField(max_length=15, null=True, blank=True)
    cha_boe = models.TextField(null=True, blank=True)
    agent_importer = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("vessel-list")
