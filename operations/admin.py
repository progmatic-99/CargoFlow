from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Company, Shipper, Consignee, Vessel, Container, Cargo, PortHandling, Voyage, BillOfLading, Manifest, looseCargo, Service, ServiceType

admin.site.register(Company)
admin.site.register(Shipper)
admin.site.register(Consignee)
admin.site.register(Vessel)
admin.site.register(Container)
admin.site.register(Cargo)
admin.site.register(PortHandling)
admin.site.register(Voyage)
admin.site.register(BillOfLading)
admin.site.register(looseCargo)

class ManifestAdmin(admin.ModelAdmin):
    readonly_fields = ('get_bill_of_lading_records',)

    def get_bill_of_lading_records(self, obj):
        bill_of_lading_records = BillOfLading.objects.filter(voyage=obj.voyage)
        links = []
        for bol in bill_of_lading_records:
            url = reverse("admin:operations_billoflading_change", args=[bol.id])
            link = format_html('<a href="{}">{}</a>', url, bol)
            links.append(link)
        return format_html('<br>'.join(links))

    get_bill_of_lading_records.short_description = 'Bill of Lading Records'

admin.site.register(Manifest, ManifestAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)
