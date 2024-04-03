from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from apps.vehicles.models import Vehicle
from apps.common.choices import VEHICLE_MAKES, VEHICLE_TYPES


class HomeView(generic.ListView):
    model = Vehicle
    template_name = "home.html"
    context_object_name = "vehicles"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        vehicle_make_query = self.request.GET.get("vehicle_make")
        vehicle_type_query = self.request.GET.get("vehicle_typ")

        if vehicle_make_query != "" and vehicle_make_query is not None:
            qs = queryset.filter(vehicle_make__icontains=vehicle_make_query)
            return qs

        if vehicle_type_query != "" and vehicle_type_query is not None:
            qs = queryset.filter(vehicle_type__contains=vehicle_type_query)
            return qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["VEHICLE_MAKES"] = VEHICLE_MAKES
        context["VEHICLE_TYPES"] = VEHICLE_TYPES
        context["total_available_vehicles"] = self.get_queryset().count()
        return context


class AboutView(generic.TemplateView):
    template_name = "about.html"
