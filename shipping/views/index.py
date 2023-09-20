from typing import Any, Dict
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from shipping.models.vessel import Vessel
from shipping.models.voyage import Voyage
from shipping.models.service import Service
from cargo.models.container import Container


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "shipping/index.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["total_vessels"] = Vessel.objects.count()

        total_containers = Container.objects.count()
        loaded_containers = Container.objects.filter(stuffed=True).count()
        empty_containers = total_containers - loaded_containers
        context["total_containers"] = total_containers
        context["loaded_containers"] = loaded_containers
        context["empty_containers"] = empty_containers

        context["incoming_vessels"] = Voyage.objects.filter(eta__isnull=False).count()
        context["outgoing_vessel"] = Voyage.objects.filter(etd__isnull=False).count()

        context["services_pending"] = Service.objects.filter(completed=False).count()

        return context
