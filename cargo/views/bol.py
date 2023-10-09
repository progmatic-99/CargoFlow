from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from cargo.models.bol import BillOfLading
from utils.create_pdf import create_pdf, create_zip
from cargo.forms import (
    BOLForm,
    BOLCreateForm,
    BOLCreateFormSet,
    BOLConstantForm,
    BOLListForm,
)
from shipping.models.voyage import Voyage
from shipping.forms import VoyageSelectionForm


class BillOfLadingCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = BillOfLading
    form_class = BOLCreateForm
    template_name = "shipping/formset.html"
    heading = "Bill of Lading"
    button_heading = "Add"
    table_headings = [
        "BL",
        "Loose Cargo",
        "Mark",
        "No of Pkg",
        "Weight",
        "Consignee",
        "Shipper",
        "Amount",
        "Description",
        "Remarks",
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = self.heading
        ctx["button_heading"] = self.button_heading
        ctx["table_headings"] = self.table_headings
        ctx["constant_form"] = BOLConstantForm()
        ctx["formset"] = BOLCreateFormSet(
            queryset=BillOfLading.objects.none(),
        )
        return ctx

    def post(self, request, *args, **kwargs):
        voyage_number = request.POST.get("voyages")
        bol_type = request.POST.get("bol_type")
        voyage = Voyage.objects.filter(voyage_number=voyage_number).first()
        data = {
            key: request.POST[key]
            for key in request.POST
            if key not in ["voyages", "bol_type"]
        }

        formset = BOLCreateFormSet(data=data)

        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.voyage = voyage
                    instance.bol_type = bol_type
                    instance.save()
        else:
            ctx = {}
            ctx["heading"] = self.heading
            ctx["button_heading"] = self.button_heading
            ctx["table_headings"] = self.table_headings
            ctx["constant_form"] = BOLConstantForm()
            ctx["formset"] = formset
            return self.render_to_response(ctx)

        return redirect(reverse_lazy("container-list"))


class BillOfLadingList(FormView):
    form_class = VoyageSelectionForm
    template_name = "cargo/bol_list.html"
    success_url = reverse_lazy("bol-list")

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        related_bols = BillOfLading.objects.filter(
            voyage=selected_voyage, loose_cargo=False
        )
        formset = BOLListForm()

        context = self.get_context_data(
            form=form,
            selected_voyage=selected_voyage,
            related_bols=related_bols,
            formset=formset,
        )
        return self.render_to_response(context)


class BillOfLadingEdit(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "index"
    model = BillOfLading
    form_class = BOLForm
    template_name = "shipping/create_form.html"


class BillOfLadingDelete(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "index"
    model = BillOfLading
    template_name = "shipping/bol_delete.html"
    success_url = reverse_lazy("index")


class BillOfLadingDownload(FormView):
    template_name = "cargo/bol.html"
    form_class = BOLListForm

    def post(self, request, slug):
        data = {
            key: request.POST[key]
            for key in request.POST.keys()
            if key not in ["csrfmiddlewaretoken", "all"]
        }

        voyage = Voyage.objects.filter(slug=slug).first()
        bol_data = []
        for bol_number, bol_slug in data.items():
            bol = BillOfLading.objects.filter(
                voyage=voyage, loose_cargo=False, slug=bol_slug
            )
            bol_data.append(bol)

        if len(bol_data) == 1:
            bol = bol_data[0].first()
            ctx = {"bol": bol_data[0], "voyage": voyage}
            return create_pdf(f"{bol.bol_number}.pdf", ctx, self.template_name)

        return create_zip(voyage, bol_data, self.template_name)
