from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.company import Company
from shipping.forms import CompanyCreateForm


class CompanyCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Company
    form_class = CompanyCreateForm
    template_name = "shipping/create_form.html"


class CompanyList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Company
    template_name = "shipping/company_list.html"
    paginate_by = 10


class CompanyEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Company
    form_class = CompanyCreateForm
    template_name = "shipping/create_form.html"


class CompanyDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Company
    template_name = "shipping/company_delete.html"
    success_url = reverse_lazy("index")
