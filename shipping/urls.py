from django.urls import path
from .views.auth import loginPage, logoutUser
from .views.index import IndexView
from .views.service import (
    ServiceCreate,
    ServiceList,
    ServiceEdit,
    ServiceDelete,
    DeliveryChallan,
    JobSheetPdf,
)
from .views.service_type import (
    ServiceTypeCreate,
    ServiceTypeEdit,
    ServiceTypeList,
    ServiceTypeDelete,
)
from .views.vessel import (
    VesselCreate,
    VesselDelete,
    VesselEdit,
    VesselList,
)
from .views.voyage import (
    VoyageCreate,
    VoyageEdit,
    VoyageList,
    VoyageDelete,
)
from .views.shipper import (
    ShipperCreate,
    ShipperDelete,
    ShipperEdit,
    ShipperList,
)
from .views.company import (
    CompanyCreate,
    CompanyDelete,
    CompanyEdit,
    CompanyList,
)
from .views.consignee import (
    ConsigneeCreate,
    ConsigneeDelete,
    ConsigneeEdit,
    ConsigneeList,
)
from .views.container import (
    ContainerCreate,
    ContainerDelete,
    ContainerEdit,
    ContainerList,
)


urlpatterns = [
    # Auth views
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("", IndexView.as_view(), name="index"),
    # service views
    path("service/create", ServiceCreate.as_view(), name="service-create"),
    path("service/list", ServiceList.as_view(), name="service-list"),
    path("service/edit/<slug:slug>", ServiceEdit.as_view(), name="service-edit"),
    path("service/delete/<slug:slug>", ServiceDelete.as_view(), name="service-delete"),
    path("service/job-sheet/<slug:slug>", JobSheetPdf.as_view(), name="job-sheet"),
    path(
        "service/delivery-challan/<slug:slug>",
        DeliveryChallan.as_view(),
        name="delivery-challan",
    ),
    # service type views
    path(
        "service-type/create", ServiceTypeCreate.as_view(), name="service-type-create"
    ),
    path("service-type/list", ServiceTypeList.as_view(), name="service-type-list"),
    path(
        "service-type/edit/<slug:slug>",
        ServiceTypeEdit.as_view(),
        name="service-type-edit",
    ),
    path(
        "service-type/delete/<slug:slug>",
        ServiceTypeDelete.as_view(),
        name="service-type-delete",
    ),
    # vessel views
    path("vessel/create", VesselCreate.as_view(), name="vessel-create"),
    path("vessel/list", VesselList.as_view(), name="vessel-list"),
    path("vessel/edit/<slug:slug>", VesselEdit.as_view(), name="vessel-edit"),
    path("vessel/delete/<slug:slug>", VesselDelete.as_view(), name="vessel-delete"),
    # voyage views
    path("voyage/create", VoyageCreate.as_view(), name="voyage-create"),
    path("voyage/list", VoyageList.as_view(), name="voyage-list"),
    path("voyage/edit/<slug:slug>", VoyageEdit.as_view(), name="voyage-edit"),
    path("voyage/delete/<slug:slug>", VoyageDelete.as_view(), name="voyage-delete"),
    # shipper views
    path("shipper/create", ShipperCreate.as_view(), name="shipper-create"),
    path("shipper/list", ShipperList.as_view(), name="shipper-list"),
    path("shipper/edit/<slug:slug>", ShipperEdit.as_view(), name="shipper-edit"),
    path("shipper/delete/<slug:slug>", ShipperDelete.as_view(), name="shipper-delete"),
    # company views
    path("company/create", CompanyCreate.as_view(), name="company-create"),
    path("company/list", CompanyList.as_view(), name="company-list"),
    path("company/edit/<slug:slug>", CompanyEdit.as_view(), name="company-edit"),
    path("company/delete/<slug:slug>", CompanyDelete.as_view(), name="company-delete"),
    # consignee views
    path("consignee/create", ConsigneeCreate.as_view(), name="consignee-create"),
    path("consignee/list", ConsigneeList.as_view(), name="consignee-list"),
    path("consignee/edit/<slug:slug>", ConsigneeEdit.as_view(), name="consignee-edit"),
    path(
        "consignee/delete/<slug:slug>",
        ConsigneeDelete.as_view(),
        name="consignee-delete",
    ),
    # container views
    path("container/create", ContainerCreate.as_view(), name="container-create"),
    path("container/list", ContainerList.as_view(), name="container-list"),
    path("container/edit/<slug:slug>", ContainerEdit.as_view(), name="container-edit"),
    path(
        "container/delete/<slug:slug>",
        ContainerDelete.as_view(),
        name="container-delete",
    ),
]
