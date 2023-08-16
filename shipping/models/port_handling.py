from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils import timezone

from .voyage import Voyage
from .container import Container
from .container import ContainerStatus


class PortHandling(models.Model):
    slug = AutoSlugField(populate_from="status", unique=True)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    Container = models.ForeignKey(Container, on_delete=models.CASCADE)
    status = models.ForeignKey(ContainerStatus, on_delete=models.CASCADE, null=True)
    status_start_time = models.DateTimeField(default=timezone.now)
    status_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.voyage.vessel.name} - ({self.status_start_time} - {self.status_end_time})"

    def status_duration(self):
        if self.status_end_time:
            return self.status_end_time - self.status_start_time
        else:
            return timezone.now() - self.status_start_time
