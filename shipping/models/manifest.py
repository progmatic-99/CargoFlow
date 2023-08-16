from django.db import models
from django_extensions.db.fields import AutoSlugField

from .voyage import Voyage
from .bol import BillOfLading


class Manifest(models.Model):
    slug = AutoSlugField(populate_from="created_at", unique=True)
    voyage = models.OneToOneField(Voyage, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manifest for {self.voyage.vessel.name} ({self.voyage.voyage_number})"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.filter(voyage=self.voyage)
