from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Company, Shipper, Consignee, Vessel, Container, Cargo, PortHandling, Voyage, BillOfLading, Manifest, looseCargo, Service, ServiceType, DeliveryOrder

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

class DeliveryOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('get_bill_of_lading_records',)

    def get_bill_of_lading_records(self, obj):
        bill_of_lading_records = BillOfLading.objects.filter(consignee=obj.consignee, voyage=obj.voyage)
        links = []
        for bol in bill_of_lading_records:
            url = reverse("admin:operations_billoflading_change", args=[bol.id])
            cargo_details = bol.cargo.description if bol.cargo else bol.loose_cargo.description
            link_text = f"{bol} - Cargo: {cargo_details}"
            link = format_html('<a href="{}">{}</a>', url, link_text)
            links.append(link)
        return format_html('<br>'.join(links))

    get_bill_of_lading_records.short_description = 'Bill of Lading Records'

admin.site.register(DeliveryOrder, DeliveryOrderAdmin)

class ManifestAdmin(admin.ModelAdmin):
    readonly_fields = ('get_bill_of_lading_records',)

    def get_bill_of_lading_records(self, obj):
        bill_of_lading_records = BillOfLading.objects.filter(voyage=obj.voyage)
        links = []
        for bol in bill_of_lading_records:
            url = reverse("admin:operations_billoflading_change", args=[bol.id])
            cargo_details = bol.cargo.description if bol.cargo else bol.loose_cargo.description
            link_text = f"{bol} - Cargo: {cargo_details}"
            link = format_html('<a href="{}">{}</a>', url, link_text)
            links.append(link)
        return format_html('<br>'.join(links))

    get_bill_of_lading_records.short_description = 'Bill of Lading Records'


admin.site.register(Manifest, ManifestAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)




