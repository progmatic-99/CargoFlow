from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from cargo.models.vendor import Vendor
from cargo.forms import VendorCreateForm


class VendorCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Vendor
    form_class = VendorCreateForm
    template_name = "shipping/create_form.html"


class VendorList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Vendor
    template_name = "cargo/vendor_list.html"
    paginate_by = 10


class VendorEdit(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vendor
    form_class = VendorCreateForm
    template_name = "shipping/create_form.html"


class VendorDelete(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vendor
    template_name = "shipping/create_form.html"
    success_url = reverse_lazy("index")
