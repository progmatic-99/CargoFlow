from datetime import timedelta

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from operations.admin_site import CustomAdminSite

from .models import (
    BillOfLading,
    Cargo,
    Company,
    Consignee,
    Container,
    ContainerStatus,
    DeliveryOrder,
    Manifest,
    PortHandling,
    Service,
    ServiceType,
    Shipper,
    Vessel,
    Voyage,
    looseCargo,
)

admin_site = CustomAdminSite(name="myadmin")


admin_site.register(Company)
admin_site.register(Shipper)
admin_site.register(Consignee)
admin_site.register(Vessel)
admin_site.register(Container)
admin_site.register(Cargo)
admin_site.register(Voyage)
admin_site.register(ContainerStatus)


class BillOfLadingAdmin(admin.ModelAdmin):
    list_display = ("bill_of_lading_number", "voyage", "consignee", "shipper")
    list_filter = ("voyage",)
    search_fields = (
        "voyage__voyage_number",
        "bill_of_lading_number",
        "consignee__contact_person",
        "shipper__contact_person",
        "cargo__description",
        "loose_cargo__description",
        "loose_cargo__color",
    )


admin_site.register(BillOfLading, BillOfLadingAdmin)


class looseCargoAdmin(admin.ModelAdmin):
    list_display = ("description", "weight", "color")
    list_filter = ("color",)


admin_site.register(looseCargo, looseCargoAdmin)


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ("consignee", "voyage", "created_at")
    readonly_fields = ("get_bill_of_lading_records",)
    list_filter = ("consignee", "voyage")
    search_fields = (
        "voyage__voyage_number",
        "consignee__contact_person",
        "consignee__billoflading__loose_cargo__color",
        "consignee__billoflading__shipper__contact_person",
        "consignee__billoflading__cargo__container__container_number",
    )

    def get_bill_of_lading_records(self, obj):
        bill_of_lading_records = BillOfLading.objects.filter(
            consignee=obj.consignee, voyage=obj.voyage
        )
        links = []
        for bol in bill_of_lading_records:
            url = reverse("admin:operations_billoflading_change", args=[bol.id])
            cargo_details = (
                bol.cargo.description if bol.cargo else bol.loose_cargo.description
            )
            link_text = f"{bol} - Cargo: {cargo_details}"
            link = format_html('<a href="{}">{}</a>', url, link_text)
            links.append(link)
        return format_html("<br>".join(links))

    get_bill_of_lading_records.short_description = "Bill of Lading Records"


admin_site.register(DeliveryOrder, DeliveryOrderAdmin)


class ManifestAdmin(admin.ModelAdmin):
    list_display = ("voyage", "created_at")
    readonly_fields = ("get_bill_of_lading_records",)

    def get_bill_of_lading_records(self, obj):
        bill_of_lading_records = BillOfLading.objects.filter(voyage=obj.voyage)
        links = []
        for bol in bill_of_lading_records:
            url = reverse("admin:operations_billoflading_change", args=[bol.id])
            cargo_details = (
                bol.cargo.description if bol.cargo else bol.loose_cargo.description
            )
            link_text = f"{bol} - Cargo: {cargo_details}"
            link = format_html('<a href="{}">{}</a>', url, link_text)
            links.append(link)
        return format_html("<br>".join(links))

    get_bill_of_lading_records.short_description = "Bill of Lading Records"


admin_site.register(Manifest, ManifestAdmin)
admin_site.register(ServiceType)
admin_site.register(Service)


class PortHandlingAdmin(admin.ModelAdmin):
    list_display = (
        "Container",
        "status",
        "status_start_time",
        "status_end_time",
        "status_duration_str",
    )
    readonly_fields = ("status_duration",)
    search_fields = ("Container__container_number",)

    def status_duration_str(self, obj):
        duration = obj.status_duration()
        duration_str = str(duration - timedelta(microseconds=duration.microseconds))
        return duration_str

    status_duration_str.short_description = "Duration"


admin_site.register(PortHandling, PortHandlingAdmin)
