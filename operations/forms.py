from .models import (
    Service,
    ServiceType,
    Vessel,
    Voyage,
    Consignee,
    Shipper,
    Company,
    Container,
    ForeignVessel,
)
from django import forms


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "service_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ServiceTypeCreateForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = "__all__"


class VesselCreateForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = "__all__"


class VoyageCreateForm(forms.ModelForm):
    class Meta:
        model = Voyage
        fields = "__all__"
        widgets = {
            "departure_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "arrival_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "last_port_departure": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }


class ConsigneeCreateForm(forms.ModelForm):
    class Meta:
        model = Consignee
        fields = "__all__"


class ShipperCreateForm(forms.ModelForm):
    class Meta:
        model = Shipper
        fields = "__all__"


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"


class ContainerCreateForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = "__all__"


class ForeignVesselCreateForm(forms.ModelForm):
    class Meta:
        model = ForeignVessel
        fields = "__all__"
