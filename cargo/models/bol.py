from django.db import models
from django_extensions.db.fields import AutoSlugField

from shipping.models.voyage import Voyage
from cargo.models.container import Container


class BillOfLading(models.Model):
    slug = AutoSlugField(populate_from="mark", unique=True)
    bol_type = models.CharField(max_length=10)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    bol_number = models.IntegerField()
    loose_cargo = models.BooleanField(default=False)
    mark = models.CharField(max_length=50, null=True)
    no_of_pkg = models.IntegerField()
    weight = models.FloatField()
    consignee = models.CharField(max_length=150)
    shipper = models.CharField(max_length=300)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bol_number} - ({self.voyage.voyage_number})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.loose_cargo:
            stuffed = False
            if self.bol_type == "1":
                stuffed = True

            Container.objects.create(
                container_number=self.mark, voyage=self.voyage, stuffed=stuffed
            )
