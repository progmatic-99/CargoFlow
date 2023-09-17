from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from models.sof import SOF
from forms import SOFCreateForm


class SOFCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = SOF
    form_class = SOFCreateForm
    template_name = "shipping/create_form.html"


class SOFList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = SOF
    template_name = "shipping/sof_list.html"
    paginate_by = 10


class SOFEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = SOF
    form_class = SOFCreateForm
    template_name = "shipping/create_form.html"


class SOFDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = SOF
    template_name = "shipping/sof_delete.html"
    success_url = reverse_lazy("index")
