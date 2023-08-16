from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.shipper import Shipper
from shipping.forms import ShipperCreateForm


class ShipperCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Shipper
    form_class = ShipperCreateForm
    template_name = "shipping/create_form.html"


class ShipperList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Shipper
    template_name = "shipping/shipper_list.html"
    paginate_by = 10


class ShipperEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Shipper
    form_class = ShipperCreateForm
    template_name = "shipping/create_form.html"


class ShipperDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Shipper
    template_name = "shipping/shipper_delete.html"
    success_url = reverse_lazy("index")
