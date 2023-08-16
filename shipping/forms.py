from .models.service import Service
from .models.service_type import ServiceType
from .models.vessel import Vessel
from .models.consignee import Consignee
from .models.shipper import Shipper
from .models.company import Company
from .models.container import Container
from .models.sof import SOF
from .models.voyage import Voyage

from django import forms


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "service_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ServiceTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True  # allow empty forms to submit

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ServiceType
        fields = ["name", "company", "price_per_tonnage", "description"]


ServiceTypeCreateFormSet = forms.modelformset_factory(
    ServiceType,
    form=ServiceTypeCreateForm,
    extra=1,
    widgets={"description": forms.Textarea(attrs={"cols": 6, "rows": 4})},
)


class VesselSelectionForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = ["name"]
        widgets = {"name": forms.Select()}


class VesselCreateForm(forms.ModelForm):
    VESSEL_TYPES = [("COASTAL", "COASTAL"), ("FOREIGN", "FOREIGN")]
    vessel_type = forms.ChoiceField(choices=VESSEL_TYPES)

    class Meta:
        model = Vessel
        fields = "__all__"


class VoyageCreateForm(forms.ModelForm):
    class Meta:
        model = Voyage
        fields = "__all__"
        widgets = {
            "etd": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "eta": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "etb": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "departed_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
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


class SOFCreateForm(forms.ModelForm):
    class Meta:
        model = SOF
        fields = "__all__"
        widgets = {
            "pilot_on_board": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "first_line_ashore": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "all_fast": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "pilot_off": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "gangway_down": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "discharging_commenced": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "discharging_completed": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "pilot_on_board_for_departure": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "tugs_line": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {"tugs_line": "Tug's Line Cast Off"}
