from django.db import models
from django_extensions.db.fields import AutoSlugField
from cargo.models.container import Container


class ContainerStatus(models.Model):
    slug = AutoSlugField(populate_from="timestamp", unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="status"
    )
