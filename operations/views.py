from typing import Any, Dict
from django.views.generic.base import TemplateView
from users.models import User
from .models import (
    Service,
    ServiceType,
    Vessel,
    Voyage,
    Consignee,
    Company,
    Shipper,
    Container,
    looseCargo,
    ForeignVessel,
)
from .forms import (
    ServiceCreateForm,
    ServiceTypeCreateForm,
    VesselCreateForm,
    VoyageCreateForm,
    ConsigneeCreateForm,
    ShipperCreateForm,
    CompanyCreateForm,
    ContainerCreateForm,
    ForeignVesselCreateForm,
)
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def loginPage(request):
    page = "login"
    error = ""

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            error = "User dont exist! Please Try Again"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # email = user.email
            return redirect("index")
        else:
            error = "Credentials dont match. Please Try Again"

    loginPage_data = {"page": page, "error": error}
    return render(request, "operations/login.html", loginPage_data)


def logoutUser(request):
    logout(request)
    return redirect("login")


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "operations/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_vessels"] = Vessel.objects.count()

        total_containers = Container.objects.count()
        context["total_containers"] = total_containers
        context["total_loose_cargo"] = looseCargo.objects.count()

        containers_on_port = Container.objects.filter(on_port=True).count()
        context["containers_on_port"] = containers_on_port

        containers_on_vessel = total_containers - containers_on_port
        context["containers_on_vessel"] = containers_on_vessel

        context["incoming_vessels"] = ForeignVessel.objects.count()
        context["vessels_on_port"] = Vessel.objects.filter(on_port=True).count()
        context["services_completed"] = Service.objects.filter(completed=True).count()
        context["outgoing_vessels"] = Vessel.objects.filter(on_port=False).count()

        services = Service.objects.all()
        total_service_revenue = 0
        for service in services:
            total_service_revenue += service.calculate_service_revenue()

        context["total_service_revenue"] = total_service_revenue

        return context


class ServiceCreate(LoginRequiredMixin, CreateView):
    # permission_required = "gobasic.add_customer"
    login_url = "/login/"
    login_required = True
    redirect_field_name = "index"
    model = Service
    form_class = ServiceCreateForm
    template_name = "operations/create_form.html"


class ServiceList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Service
    template_name = "operations/service_list.html"
    paginate_by = 10


class ServiceEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    form_class = ServiceCreateForm
    template_name = "operations/create_form.html"


class ServiceDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Service
    template_name = "operations/service_delete.html"
    success_url = reverse_lazy("index")


class ServiceTypeCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = ServiceType
    form_class = ServiceTypeCreateForm
    template_name = "operations/create_form.html"


class ServiceTypeList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = ServiceType
    template_name = "operations/service_type_list.html"
    paginate_by = 10


class ServiceTypeEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ServiceType
    form_class = ServiceTypeCreateForm
    template_name = "operations/create_form.html"


class ServiceTypeDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ServiceType
    template_name = "operations/service_type_delete.html"
    success_url = reverse_lazy("index")


class VesselCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Vessel
    form_class = VesselCreateForm
    template_name = "operations/create_form.html"


class VesselList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Vessel
    template_name = "operations/vessel_list.html"
    paginate_by = 10


class VesselEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vessel
    form_class = VesselCreateForm
    template_name = "operations/create_form.html"


class VesselDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Vessel
    template_name = "operations/vessel_delete.html"
    success_url = reverse_lazy("index")


class VoyageCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Voyage
    form_class = VoyageCreateForm
    template_name = "operations/create_form.html"


class VoyageList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Voyage
    template_name = "operations/voyage_list.html"
    paginate_by = 10


class VoyageEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Voyage
    form_class = VoyageCreateForm
    template_name = "operations/create_form.html"


class VoyageDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Voyage
    template_name = "operations/voyage_delete.html"
    success_url = reverse_lazy("index")


class ConsigneeCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Consignee
    form_class = ConsigneeCreateForm
    template_name = "operations/create_form.html"


class ConsigneeList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Consignee
    template_name = "operations/consignee_list.html"
    paginate_by = 10


class ConsigneeEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Consignee
    form_class = ConsigneeCreateForm
    template_name = "operations/create_form.html"


class ConsigneeDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Consignee
    template_name = "operations/consignee_delete.html"
    success_url = reverse_lazy("index")


class CompanyCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Company
    form_class = CompanyCreateForm
    template_name = "operations/create_form.html"


class CompanyList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Company
    template_name = "operations/company_list.html"
    paginate_by = 10


class CompanyEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Company
    form_class = CompanyCreateForm
    template_name = "operations/create_form.html"


class CompanyDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Company
    template_name = "operations/company_delete.html"
    success_url = reverse_lazy("index")


class ShipperCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Shipper
    form_class = ShipperCreateForm
    template_name = "operations/create_form.html"


class ShipperList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Shipper
    template_name = "operations/shipper_list.html"
    paginate_by = 10


class ShipperEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Shipper
    form_class = ShipperCreateForm
    template_name = "operations/create_form.html"


class ShipperDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Shipper
    template_name = "operations/shipper_delete.html"
    success_url = reverse_lazy("index")


class ContainerCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = Container
    form_class = ContainerCreateForm
    template_name = "operations/create_form.html"


class ContainerList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = Container
    template_name = "operations/container_list.html"
    paginate_by = 10


class ContainerEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    form_class = ContainerCreateForm
    template_name = "operations/create_form.html"


class ContainerDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = Container
    template_name = "operations/container_delete.html"
    success_url = reverse_lazy("index")


class ForeignVesselCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = "index"
    model = ForeignVessel
    form_class = ForeignVesselCreateForm
    template_name = "operations/create_form.html"


class ForeignVesselList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "index"
    login_required = True
    model = ForeignVessel
    template_name = "operations/foreign_vessel_list.html"
    paginate_by = 10


class ForeignVesselEdit(LoginRequiredMixin, UpdateView):
    # permission_required = "gobasic.change_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ForeignVessel
    form_class = ForeignVesselCreateForm
    template_name = "operations/create_form.html"


class ForeignVesselDelete(LoginRequiredMixin, DeleteView):
    # permission_required = "gobasic.delete_customer"
    login_url = "/login/"
    redirect_field_name = "index"
    model = ForeignVessel
    template_name = "operations/foreign_vessel_delete.html"
    success_url = reverse_lazy("index")
