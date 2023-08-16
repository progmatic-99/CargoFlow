from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from datetime import datetime

from .vessel import Vessel
from .voyage import Voyage
from .service_type import ServiceType


class ServiceManager(models.Manager):
    def services_for_vessel(self, vessel):
        return self.filter(vessel=vessel)


class Service(models.Model):
    slug = AutoSlugField(populate_from="service_date", unique=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, null=True)
    service_type = models.ManyToManyField(ServiceType)
    service_date = models.DateTimeField(default=datetime.now())
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    objects = ServiceManager()

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_type.name} for {self.vessel.name}"

    def get_absolute_url(self):
        return reverse("service-list")

    def calculate_service_revenue(self):
        total_revenue = 0

        for service_type in self.service_type.all():
            total_revenue += service_type.price_per_tonnage

        return round(total_revenue, 2)
