from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


VESSEL_TYPES = [("COASTAL", "COASTAL"), ("FOREIGN", "FOREIGN")]
CATEGORIES = [
    ("CARGO", "CARGO"),
    ("PASSENGER", "PASSENGER"),
    ("NAVY", "NAVY"),
    ("TUG/OSV", "TUG/OSV"),
    ("TANKERS", "TANKERS"),
    ("YACHT", "YACHT"),
    ("OTHERS", "OTHERS"),
]


class Vessel(models.Model):
    slug = AutoSlugField(populate_from="imo_number", unique=True)
    name = models.CharField(max_length=200)
    vessel_type = models.CharField(max_length=20, choices=VESSEL_TYPES)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    imo_number = models.CharField(max_length=15)
    flag = models.CharField(max_length=50)
    call_sign = models.CharField(max_length=200)
    official_no = models.IntegerField()
    registry_port = models.CharField(max_length=200)
    mmsi = models.FloatField()
    loa = models.FloatField()
    beam = models.FloatField()
    depth = models.FloatField()
    length = models.FloatField()
    breadth = models.FloatField()
    charter_type = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}-{self.vessel_type}"

    def get_absolute_url(self):
        return reverse("vessel-list")
