from django.contrib import admin
from .models import (
    looseCargo,
    BillOfLading,
    Container,
    ContainerStatus,
    DeliveryOrder,
    Manifest,
    Vendor,
)

admin.site.register(looseCargo)
admin.site.register(BillOfLading)
admin.site.register(Container)
admin.site.register(ContainerStatus)
admin.site.register(DeliveryOrder)
admin.site.register(Manifest)
admin.site.register(Vendor)
