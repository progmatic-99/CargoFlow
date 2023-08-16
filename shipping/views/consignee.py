from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.consignee import Consignee
from shipping.forms import ConsigneeCreateForm


class ConsigneeCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Consignee
    form_class = ConsigneeCreateForm
    template_name = "shipping/create_form.html"


class ConsigneeList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Consignee
    template_name = "shipping/consignee_list.html"
    paginate_by = 10


class ConsigneeEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Consignee
    form_class = ConsigneeCreateForm
    template_name = "shipping/create_form.html"


class ConsigneeDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Consignee
    template_name = "shipping/consignee_delete.html"
    success_url = reverse_lazy("index")
