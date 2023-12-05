from cargo.models.bol import BillOfLading
from cargo.models.vendor import Vendor
from cargo.models.container import Container
from shipping.forms import VoyageSelectionForm

from django import forms


TYPE = [(1, "IMPORT"), (2, "EXPORT")]


class ContainerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["container_number"].disabled = True

    class Meta:
        model = Container
        fields = ["container_number", "stuffed"]


ContainerFormSet = forms.modelformset_factory(Container, form=ContainerForm, extra=0)


class VendorCreateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        labels = {"ifsc_code": "IFSC Code"}
        fields = "__all__"


class BOLForm(forms.ModelForm):
    class Meta:
        model = BillOfLading
        exclude = ["voyage", "bol_type"]


class CheckboxForm(forms.Form):
    select = forms.BooleanField()


class BOLCreateForm(BOLForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = True


BOLCreateFormSet = forms.modelformset_factory(
    BillOfLading,
    form=BOLCreateForm,
    extra=1,
)


class BOLConstantForm(VoyageSelectionForm):
    bol_type = forms.ChoiceField(label="BOL type", choices=TYPE, required=True)
