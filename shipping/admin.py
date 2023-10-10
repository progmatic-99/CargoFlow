from django.contrib import admin
from .models import Vessel, Voyage, Service, ServiceType, SOF

admin.site.register(Vessel)
admin.site.register(Voyage)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(SOF)




