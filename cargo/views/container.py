from django.views.generic.edit import DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from cargo.models.container import Container
from shipping.forms import VoyageSelectionForm
from shipping.models.voyage import Voyage
from cargo.forms import ContainerFormSet


class ContainerList(LoginRequiredMixin, FormView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    template_name = "cargo/container_list.html"
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        related_containers = Container.objects.filter(voyage=selected_voyage).all()
        formset = ContainerFormSet(queryset=related_containers)

        context = self.get_context_data(
            form=form,
            total_containers=related_containers.count(),
            selected_voyage=selected_voyage,
            formset=formset,
        )

        return self.render_to_response(context)


class ContainerEdit(LoginRequiredMixin, FormView):
    login_url = "/login/"
    redirect_field_name = "index"
    template_name = "cargo/container_list.html"

    def post(self, request, *args, **kwargs):
        formset = ContainerFormSet(data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
        else:
            ctx = {}
            ctx["form"] = VoyageSelectionForm()
            ctx["formset"] = formset
            return self.render_to_response(ctx)

        return redirect(reverse_lazy("container-list"))


class ContainerDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    template_name = "shipping/container_delete.html"
    success_url = reverse_lazy("index")
