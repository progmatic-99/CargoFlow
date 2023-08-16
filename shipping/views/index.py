from typing import Any, Dict
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.vessel import Vessel
from shipping.models.voyage import Voyage
from shipping.models.service import Service
from shipping.models.loose_cargo import looseCargo
from shipping.models.container import Container


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "shipping/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_vessels"] = Vessel.objects.count()

        total_containers = Container.objects.count()
        context["total_containers"] = total_containers
        context["total_loose_cargo"] = looseCargo.objects.count()

        context["incoming_vessels"] = Voyage.objects.filter(eta__isnull=False).count()
        context["outgoing_vessel"] = Voyage.objects.filter(etd__isnull=False).count()

        context["services_pending"] = Service.objects.filter(completed=False).count()

        return context
