from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.voyage import Voyage
from cargo.models.bol import BillOfLading
from utils.create_pdf import create_pdf


class ManifestPDF(LoginRequiredMixin, ListView):
    template_name = "cargo/manifest.html"

    def get(self, request, slug):
        voyage = Voyage.objects.filter(slug=slug).first()
        filename = f"{voyage.voyage_number}-manifest.pdf"

        related_bols = BillOfLading.objects.filter(voyage=voyage).all()

        bol_type = "IMPORT" if related_bols[0].bol_type == "1" else "EXPORT"

        ctx = {
            "voyage": voyage,
            "vessel": voyage.vessel,
            "type": bol_type,
            "related_bols": related_bols,
        }

        return create_pdf(filename, ctx, self.template_name)
