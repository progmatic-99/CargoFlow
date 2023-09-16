from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

from .voyage import Voyage


class SOF(models.Model):
    slug = AutoSlugField(populate_from="", unique=True)
    eosp = models.CharField(max_length=200)
    nor_tendered = models.CharField(max_length=200)
    pilot_on_board = models.DateTimeField()
    first_line_ashore = models.DateTimeField()
    all_fast = models.DateTimeField()
    pilot_off = models.DateTimeField()
    gangway_down = models.DateTimeField()
    discharging_commenced = models.DateTimeField()
    discharging_completed = models.DateTimeField()
    pilot_on_board_for_departure = models.DateTimeField()
    tugs_line = models.DateTimeField()
    vessel_shifting = models.TextField(blank=True, null=True)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Statement of Facts"

    def get_absolute_url(self):
        return reverse("statement-of-facts")
