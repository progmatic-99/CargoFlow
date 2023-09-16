from django.db import models
from django_extensions.db.fields import AutoSlugField

from shipping.models.voyage import Voyage
from cargo.models.bol import BillOfLading


class Manifest(models.Model):
    slug = AutoSlugField(populate_from="voyage.voyage_number", unique=True)
    voyage = models.OneToOneField(Voyage, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Manifest for {self.voyage} ({self.voyage.voyage_number})"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.filter(voyage=self.voyage)
