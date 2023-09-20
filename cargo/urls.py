from django.urls import path
from .views.container import ContainerList, ContainerEdit
from .views.bol import (
    BillOfLadingCreate,
    BillOfLadingList,
    BillOfLadingEdit,
    BillOfLadingDelete,
)
from .views.vendor import VendorCreate, VendorDelete, VendorEdit, VendorList
from .views.manifest import ManifestPDF
from .views.delivery_order import DeliveryOrderList, DeliveryOrderPdf


urlpatterns = [
    # container views
    path("container/list", ContainerList.as_view(), name="container-list"),
    path("container/edit", ContainerEdit.as_view(), name="container-edit"),
    # bol views
    path("bol/create", BillOfLadingCreate.as_view(), name="bol-create"),
    path("bol/list", BillOfLadingList.as_view(), name="bol-list"),
    path("bol/edit/<slug:slug>", BillOfLadingEdit.as_view(), name="bol-edit"),
    path(
        "bol/delete/<slug:slug>",
        BillOfLadingDelete.as_view(),
        name="bol-delete",
    ),
    # vendor views
    path("vendor/create", VendorCreate.as_view(), name="vendor-create"),
    path("vendor/list", VendorList.as_view(), name="vendor-list"),
    path("vendor/edit/<slug:slug>", VendorEdit.as_view(), name="vendor-edit"),
    path(
        "vendor/delete/<slug:slug>",
        VendorDelete.as_view(),
        name="vendor-delete",
    ),
    # manifest pdf
    path("manifest/get/<slug:slug>", ManifestPDF.as_view(), name="get-manifest"),
    # delivery order
    path("do/list", DeliveryOrderList.as_view(), name="delivery-order-list"),
    path(
        "do/pdf/<str:consignee>",
        DeliveryOrderPdf.as_view(),
        name="delivery-order-pdf",
    ),
]
