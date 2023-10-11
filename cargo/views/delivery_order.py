from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from shipping.models.voyage import Voyage
from cargo.models.bol import BillOfLading
from cargo.forms import CheckboxForm
from shipping.forms import VoyageSelectionForm
from utils.create_pdf import create_pdf, create_do_zip
import operator
import itertools


class DeliveryOrderList(FormView):
    template_name = "cargo/delivery_order_list.html"
    success_url = reverse_lazy("delivery-order-list")
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()

        attr_name = "consignee"
        all_instances = BillOfLading.objects.all().order_by(attr_name)
        keyfunc = operator.attrgetter(attr_name)
        bol_list = [
            {"consignee": k, "bols": list(g)}
            for k, g in itertools.groupby(all_instances, keyfunc)
        ]

        context = self.get_context_data(
            checkbox_form=CheckboxForm(),
            form=form,
            selected_voyage=selected_voyage,
            bol_list=bol_list,
        )
        return self.render_to_response(context)


class DeliveryOrderPdf(LoginRequiredMixin, ListView):
    template_name = "cargo/delivery_order.html"

    def get(self, request, consignee):
        bols = BillOfLading.objects.filter(consignee=consignee).all()

        voyage = bols[0].voyage

        filename = f"{consignee}-Delivery-Order.pdf"
        ctx = {
            "bols": bols,
            "voyage": voyage,
            "consignee": consignee,
        }

        return create_pdf(filename, ctx, self.template_name)


class DeliveryOrderDownload(FormView):
    template_name = "cargo/delivery_order.html"
    form_class = CheckboxForm

    def post(self, request):
        consignees = request.POST.getlist("consignee")
        bol_data = []

        for consignee in consignees:
            bols = BillOfLading.objects.filter(consignee=consignee).all()
            bol_data.append(bols)

        voyage = bol_data[0][0].voyage
        filename = f"{voyage}-delivery-orders.zip"

        return create_do_zip(voyage, bol_data, filename, self.template_name)
