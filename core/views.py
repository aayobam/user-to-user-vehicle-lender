from typing import Any
from django.views.generic import TemplateView

from apps.common.choices import VEHICLE_MAKES, VEHICLE_TYPES


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["VEHICLE_TYPES"] = VEHICLE_TYPES
        context["VEHICLE_MAKES"] = VEHICLE_MAKES
        return context


class AboutView(TemplateView):
    template_name = "about.html"
