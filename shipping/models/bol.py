from django.db import models
from django_extensions.db.fields import AutoSlugField

from .voyage import Voyage
from .cargo import Cargo
from .consignee import Consignee
from .shipper import Shipper
from .loose_cargo import looseCargo


class BillOfLading(models.Model):
    slug = AutoSlugField(populate_from="bill_of_lading_number", unique=True)
    bill_of_lading_number = models.CharField(max_length=50)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    loose_cargo = models.ForeignKey(
        looseCargo, on_delete=models.CASCADE, blank=True, null=True
    )
    issued_date = models.DateTimeField()

    def __str__(self):
        return f"{self.bill_of_lading_number} - ({self.voyage.voyage_number})"
