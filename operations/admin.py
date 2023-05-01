from django.contrib import admin
from .models import Company, Shipper, Consignee, Vessel, Container, Cargo, looseCargo, PortHandling, Voyage, BillOfLading
# Register your models here.

admin.site.register(Company)
admin.site.register(Shipper)
admin.site.register(Consignee)
admin.site.register(Vessel)
admin.site.register(Container)
admin.site.register(Cargo)
admin.site.register(looseCargo)
admin.site.register(PortHandling)
admin.site.register(Voyage)
admin.site.register(BillOfLading)




