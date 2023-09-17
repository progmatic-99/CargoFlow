from django.db import models
from django_extensions.db.fields import AutoSlugField

from .bol import BillOfLading
from shipping.models.voyage import Voyage


class DeliveryOrder(models.Model):
    slug = AutoSlugField(populate_from="order_number", unique=True)
    order_number = models.CharField(max_length=50)
    issued_date = models.DateTimeField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    bol = models.ForeignKey(BillOfLading, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Delivery Orders"

    def __str__(self):
        return f"Delivery Order for {self.bol.consignee} - {self.voyage}"
