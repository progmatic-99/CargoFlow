from .models import (
    Service,
    ServiceType,
    Vessel,
    Voyage,
    Consignee,
    Shipper,
    Company,
    Container,
)
from django import forms


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


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
