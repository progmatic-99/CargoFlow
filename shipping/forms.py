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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True

        # Remove labels from the fields
        for field_name, field in self.fields.items():
            field.label = ""

    class Meta:
        model = Service
        fields = [
            "vessel",
            "voyage",
            "service_type",
            "service_date",
            "description",
            "completed",
        ]
        widgets = {
            "service_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "service_type": forms.Select(),
        }


ServiceCreateFormSet = forms.modelformset_factory(
    Service,
    form=ServiceCreateForm,
    extra=1,
)


class ServiceTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True  # allow empty forms to submit

        for field_name, field in self.fields.items():
            field.label = ""

    class Meta:
        model = ServiceType
        fields = ["name", "company", "price_per_tonnage", "description"]


ServiceTypeCreateFormSet = forms.modelformset_factory(
    ServiceType,
    form=ServiceTypeCreateForm,
    extra=1,
    widgets={"description": forms.Textarea(attrs={"cols": 6, "rows": 4})},
)


class VesselSelectionServiceForm(forms.ModelForm):
    class Meta:
        model = Voyage
        exclude = ["all"]


class VesselCreateForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = "__all__"
        labels = {"loa": "LOA", "beam": "BEAM", "mmsi": "MMSI", "imo_number": "IMO No"}


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
        labels = {
            "etd": "ETD",
            "eta": "ETA",
            "etb": "ETB",
            "grt": "GRT",
            "nrt": "NRT",
            "cha_boe": "CHA BOE",
            "import_no": "Import No",
            "export_no": "Export No",
        }
        fields = [
            "voyage_number",
            "vessel",
            "to_port",
            "next_port_of_call",
            "last_port_of_call",
            "master_name",
            "eta",
            "etb",
            "etd",
            "grt",
            "nrt",
            "draft",
            "owner",
            "pi_club",
            "purpose_of_call",
            "import_no",
            "export_no",
            "cha_boe",
            "agent_importer",
            "remarks",
            "vessel_on_port",
            "vessel_on_anchorage",
        ]


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
        labels = {"ifsc_code": "IFSC Code"}


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
