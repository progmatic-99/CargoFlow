from cargo.models.container import Container
from cargo.models.bol import BillOfLading
from cargo.models.vendor import Vendor
from shipping.forms import VoyageSelectionForm

from django import forms


TYPE = [(1, "IMPORT"), (2, "EXPORT")]


class ContainerCreateForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = "__all__"


class VendorCreateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        labels = {"ifsc_code": "IFSC Code"}
        fields = "__all__"


class BOLForm(forms.ModelForm):
    class Meta:
        model = BillOfLading
        exclude = ["voyage", "bol_type"]


class BOLCreateForm(BOLForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True

        # Remove labels from the fields
        for field_name, field in self.fields.items():
            field.label = ""
            field.widget.attrs["class"] = "form-control"


BOLCreateFormSet = forms.modelformset_factory(
    BillOfLading,
    form=BOLCreateForm,
    extra=1,
)


class BOLConstantForm(VoyageSelectionForm):
    bol_type = forms.ChoiceField(label="BOL type", choices=TYPE, required=True)
