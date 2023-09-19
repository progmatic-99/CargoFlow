from shipping.models.service import Service
from shipping.models.service_type import ServiceType
from shipping.models.vessel import Vessel
from shipping.models.company import Company
from shipping.models.sof import SOF
from shipping.models.voyage import Voyage

from django import forms


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "service_type",
            "service_date",
            "description",
            "completed",
        ]
        widgets = {
            "service_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "service_type": forms.Select(),
        }


class ServiceCreateForm(ServiceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True

        # Remove labels from the fields
        for field_name, field in self.fields.items():
            field.label = ""
            field.widget.attrs["class"] = "form-control"


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
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = ServiceType
        fields = ["name", "price_per_tonnage", "description"]


ServiceTypeCreateFormSet = forms.modelformset_factory(
    ServiceType,
    form=ServiceTypeCreateForm,
    extra=1,
    widgets={"description": forms.Textarea(attrs={"cols": 6, "rows": 4})},
)


class VoyageSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for obj in Voyage.objects.all():
            number = obj.voyage_number
            name = obj.__str__()
            choices.append((number, name))
            self.fields["voyages"].choices = choices

    voyages = forms.ChoiceField(label="Select a Voyage", choices=(), required=True)


class CompanySelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for obj in Company.objects.all():
            name = obj.name
            choices.append((name, name))
            self.fields["company"].choices = choices

    company = forms.ChoiceField(label="Select a Company", choices=(), required=True)


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
            "pi_club": "PI Club",
            "agent_importer": "Agent Importer",
            "purpose_of_call": "Purpose of Call",
            "charter_type": "Charter Type",
        }
        fields = "__all__"


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        labels = {"ifsc_code": "IFSC Code"}


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
