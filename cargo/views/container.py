from django.views.generic.edit import DeleteView, FormView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from cargo.models.container import Container
from shipping.forms import VoyageSelectionForm
from shipping.models.voyage import Voyage
from cargo.forms import ContainerFormSet
from cargo.models.container_status import ContainerStatus


class ContainerReport(LoginRequiredMixin, FormView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    template_name = "cargo/container_report.html"
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        related_containers = Container.objects.filter(voyage=selected_voyage).all()

        context = self.get_context_data(
            form=form,
            total_containers=related_containers.count(),
            selected_voyage=selected_voyage,
            containers=related_containers,
        )

        return self.render_to_response(context)


class ContainerList(LoginRequiredMixin, FormView):
    template_name = "cargo/container_list.html"

    def get_context_data(self, **kwargs):
        formset = ContainerFormSet(queryset=Container.objects.all())
        ctx = {"formset": formset}

        return ctx

    def post(self, request):
        print(f"Request: {request.POST}")
        formset = ContainerFormSet(data=request.POST)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if "stuffed" in form.changed_data:
                        status = bool(form.cleaned_data["stuffed"])
                        container_number = form.cleaned_data["container_number"]
                        container = Container.objects.filter(
                            container_number=container_number
                        ).first()
                        ContainerStatus.objects.create(
                            container=container,
                            status=status,
                        )
                    form.save()
        else:
            self.render_to_response(formset)

        return redirect(reverse_lazy("container-list"))


class ContainerDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    template_name = "shipping/container_delete.html"
    success_url = reverse_lazy("index")


class ContainerStatusList(LoginRequiredMixin, ListView):
    template_name = "cargo/container_status.html"
    model = Container

    def get_context_data(self, **kwargs):
        containers = Container.objects.all()
        ctx = {"containers": containers}

        return ctx
