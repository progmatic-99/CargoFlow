from django.db import models
from django_extensions.db.fields import AutoSlugField

from .bol import BillOfLading
from .consignee import Consignee
from .voyage import Voyage


class DeliveryOrder(models.Model):
    slug = AutoSlugField(populate_from="order_number", unique=True)
    order_number = models.CharField(max_length=50)
    issued_date = models.DateTimeField()
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Delivery Orders"

    def __str__(self):
        return f"Delivery Order for {self.consignee} - {self.voyage}"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.select_related(
            "cargo", "loose_cargo", "shipper", "consignee", "voyage"
        ).filter(consignee=self.consignee, voyage=self.voyage)
