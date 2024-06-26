from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.vessel import Vessel
from shipping.forms import VesselCreateForm
from typing import Any, Dict


class VesselCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Vessel
    form_class = VesselCreateForm
    template_name = "shipping/create_form.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        ctx["heading"] = "Vessel Registration"

        return ctx


class VesselList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Vessel
    template_name = "shipping/vessel_list.html"
    paginate_by = 10


class VesselEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vessel
    form_class = VesselCreateForm
    template_name = "shipping/create_form.html"


class VesselDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vessel
    template_name = "shipping/vessel_delete.html"
    success_url = reverse_lazy("index")
