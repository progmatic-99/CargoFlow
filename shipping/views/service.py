from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect
from django.template.loader import render_to_string
import weasyprint

from shipping.models.service import Service
from shipping.models.vessel import Vessel
from shipping.models.voyage import Voyage
from shipping.forms import (
    ServiceCreateForm,
    VesselSelectionServiceForm,
    ServiceCreateFormSet,
)
from rms.settings import BASE_DIR


class ServiceCreate(LoginRequiredMixin, CreateView):
    # permission_required = "gobasic.add_customer"
    login_url = "/login/"
    login_required = True
    redirect_field_name = "index"
    model = Service
    form_class = ServiceCreateForm
    template_name = "shipping/formset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Service Registration"
        context["button_heading"] = "Add Service"
        context["table_headings"] = [
            "Vessel",
            "Voyage",
            "Service Type",
            "Service Date",
            "Description",
            "Completed",
        ]
        context["formset"] = ServiceCreateFormSet(
            queryset=Service.objects.none(),
        )
        return context

    def post(self, request, *args, **kwargs):
        formset = ServiceCreateFormSet(data=request.POST)

        for form in formset:
            if form.is_valid():
                form.save()
            else:
                return self.render_to_response({"formset": formset})

        return redirect(reverse_lazy("service-list"))


class ServiceList(FormView):
    template_name = "shipping/service_list.html"
    form_class = VesselSelectionServiceForm
    success_url = reverse_lazy("service-list")

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(name=form.cleaned_data["name"]).first()
        related_services = Service.objects.filter(voyage=selected_voyage).order_by(
            "-service_date"
        )
        context = self.get_context_data(
            form=form,
            selected_voyage=selected_voyage,
            related_services=related_services,
        )
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voyages"] = Voyage.objects.all()
        return context


class ServiceEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    form_class = ServiceCreateForm
    template_name = "shipping/create_form.html"


class ServiceDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    template_name = "shipping/service_delete.html"
    success_url = reverse_lazy("index")


class DeliveryChallan(LoginRequiredMixin, ListView):
    pass


class JobSheetPdf(LoginRequiredMixin, ListView):
    template_name = "shipping/pdf/service_report.html"

    def get(self, request, slug):
        voyage = Voyage.objects.filter(slug=slug).first()

        # write logic for what if voyage doesn't exist
        if voyage:
            vessel = voyage.vessel

            related_services = Service.objects.filter(vessel=vessel).order_by(
                "-service_date"
            )
            ctx = {
                "voyage": voyage,
                "vessel": vessel,
                "related_services": related_services,
            }
            html_content = render_to_string(self.template_name, ctx).encode("utf-8")

            response = HttpResponse(content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{voyage.voyage_number}-job-sheet.pdf"'
            weasyprint.HTML(string=html_content).write_pdf(
                response,
                stylesheets=[
                    weasyprint.CSS(
                        f"{BASE_DIR}/shipping/static/shipping/css/sb-admin-2.min.css"
                    )
                ],
            )

            return response
