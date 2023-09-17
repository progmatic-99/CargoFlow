from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from cargo.models.container import Container
from cargo.forms import ContainerCreateForm
from shipping.forms import VoyageSelectionForm
from shipping.models.voyage import Voyage
from cargo.models.bol import BillOfLading


class ContainerCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Container
    form_class = ContainerCreateForm
    template_name = "shipping/create_form.html"


class ContainerList(FormView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    template_name = "cargo/container_list.html"
    paginate_by = 10
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        related_bols = BillOfLading.objects.filter(voyage=selected_voyage).all()
        context = self.get_context_data(
            form=form,
            selected_voyage=selected_voyage,
            related_bols=related_bols,
        )
        return self.render_to_response(context)


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
