from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.voyage import Voyage
from shipping.forms import VoyageCreateForm


class VoyageCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Voyage
    form_class = VoyageCreateForm
    template_name = "shipping/create_form.html"


class VoyageList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Voyage
    template_name = "shipping/voyage_list.html"
    paginate_by = 10


class VoyageEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Voyage
    form_class = VoyageCreateForm
    template_name = "shipping/create_form.html"


class VoyageDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Voyage
    template_name = "shipping/voyage_delete.html"
    success_url = reverse_lazy("index")
