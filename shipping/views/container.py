from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.container import Container
from shipping.forms import ContainerCreateForm


class ContainerCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Container
    form_class = ContainerCreateForm
    template_name = "shipping/create_form.html"


class ContainerList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Container
    template_name = "shipping/container_list.html"
    paginate_by = 10


class ContainerEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    form_class = ContainerCreateForm
    template_name = "shipping/create_form.html"


class ContainerDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    template_name = "shipping/container_delete.html"
    success_url = reverse_lazy("index")
