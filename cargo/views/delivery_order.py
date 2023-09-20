from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.voyage import Voyage
from cargo.models.bol import BillOfLading
from shipping.forms import VoyageSelectionForm
from utils.create_pdf import create_pdf


class DeliveryOrderList(FormView):
    template_name = "cargo/delivery_order_list.html"
    success_url = reverse_lazy("delivery-order-list")
    form_class = VoyageSelectionForm

    def form_valid(self, form):
        selected_voyage = Voyage.objects.filter(
            voyage_number=form.cleaned_data["voyages"]
        ).first()
        bols = BillOfLading.objects.filter(voyage=selected_voyage).all()
        context = self.get_context_data(
            form=form,
            selected_voyage=selected_voyage,
            bols=bols,
        )
        return self.render_to_response(context)


class DeliveryOrderPdf(LoginRequiredMixin, ListView):
    template_name = "cargo/delivery_order.html"

    def get(self, request, consignee):
        bols = BillOfLading.objects.filter(consignee=consignee).all()

        voyage = bols[0].voyage
        print(voyage)

        filename = f"{consignee}-delivery-order.pdf"
        ctx = {
            "bols": bols,
            "voyage": voyage,
            "consignee": consignee,
        }

        return create_pdf(filename, ctx, self.template_name)
