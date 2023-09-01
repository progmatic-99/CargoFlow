from typing import Any, Dict
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


from shipping.models.service_type import ServiceType
from shipping.forms import ServiceTypeCreateForm, ServiceTypeCreateFormSet


class ServiceTypeCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = ServiceType
    form_class = ServiceTypeCreateForm
    template_name = "shipping/formset.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "Service Type Registration"
        context["button_heading"] = "Add Service Type"
        context["table_headings"] = [
            "Name",
            "Company",
            "Price per tonnage",
            "Description",
        ]
        context["formset"] = ServiceTypeCreateFormSet(
            queryset=ServiceType.objects.none(),
            initial=[
                {
                    "name": "",
                    "price_per_tonnage": 0.0,
                    "description": "",
                    "company": None,
                }
            ],
        )
        return context

    def post(self, request, *args, **kwargs):
        formset = ServiceTypeCreateFormSet(data=request.POST)

        for form in formset:
            if form.is_valid():
                form.save()
            else:
                return self.render_to_response({"formset": formset})

        return redirect(reverse_lazy("service-type-list"))


class ServiceTypeList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = ServiceType
    template_name = "shipping/service_type_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        object_list = ServiceType.objects.all().order_by("-id")
        ctx["object_list"] = object_list

        return ctx


class ServiceTypeEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ServiceType
    form_class = ServiceTypeCreateForm
    template_name = "shipping/create_form.html"


class ServiceTypeDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ServiceType
    template_name = "shipping/service_type_delete.html"
    success_url = reverse_lazy("index")
