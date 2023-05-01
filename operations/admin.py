from django.contrib import admin
from .models import Company, Shipper, Consignee, Vessel, Container, Cargo, PortHandling
# Register your models here.

admin.site.register(Company)
admin.site.register(Shipper)
admin.site.register(Consignee)
admin.site.register(Vessel)
admin.site.register(Container)
admin.site.register(Cargo)
admin.site.register(PortHandling)




