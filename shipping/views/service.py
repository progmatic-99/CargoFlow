from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from utils.create_pdf import create_pdf
from shipping.models.service import Service
from shipping.models.voyage import Voyage
from shipping.forms import (
    ServiceForm,
    ServiceCreateForm,
    VoyageSelectionForm,
    ServiceCreateFormSet,
)


class ServiceCreate(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    login_required = True
    form_class = ServiceCreateForm
    template_name = "shipping/formset.html"
    heading = "Job Sheet"
    button_heading = "Add Service"
    table_headings = [
        "Service Type",
        "Service Date",
        "Description",
        "Completed",
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = self.heading
        ctx["button_heading"] = self.button_heading
        ctx["table_headings"] = self.table_headings
        ctx["constant_form"] = VoyageSelectionForm()
        ctx["formset"] = ServiceCreateFormSet(
            queryset=Service.objects.none(),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        voyage_number = request.POST.get("voyages")
        voyage = Voyage.objects.filter(voyage_number=voyage_number).first()
        data = {key: request.POST[key] for key in request.POST if key != "voyages"}

        formset = ServiceCreateFormSet(data=data)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.voyage = voyage
                    instance.save()
        else:
            ctx = {}
            ctx["heading"] = self.heading
            ctx["button_heading"] = self.button_heading
            ctx["table_headings"] = self.table_headings
            ctx["constant_form"] = VoyageSelectionForm()
            ctx["formset"] = formset
            return self.render_to_response(ctx)

        return redirect(reverse_lazy("service-list"))


class ServiceList(FormView):
    template_name = "shipping/service_list.html"
    success_url = reverse_lazy("service-list")
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        related_services = Service.objects.services_for_vessel(voyage=selected_voyage)
        context = self.get_context_data(
            form=form,
            selected_voyage=selected_voyage,
            related_services=related_services,
        )
        return self.render_to_response(context)


class ServiceEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    form_class = ServiceForm
    template_name = "shipping/create_form.html"


class ServiceDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    template_name = "shipping/service_delete.html"
    success_url = reverse_lazy("index")


class DeliveryChallan(LoginRequiredMixin, ListView):
    template_name = "shipping/pdf/delivery_challan.html"

    def get(self, request, slug):
        ...


class JobSheetPdf(LoginRequiredMixin, ListView):
    template_name = "shipping/pdf/service_report.html"

    def get(self, request, slug):
        voyage = Voyage.objects.filter(slug=slug).first()

        related_services = Service.objects.filter(voyage=voyage)

        filename = f"{voyage.voyage_number}-job-sheet.pdf"
        ctx = {
            "voyage": voyage,
            "vessel": voyage.vessel,
            "related_services": related_services,
        }

        return create_pdf(filename, ctx, self.template_name)
