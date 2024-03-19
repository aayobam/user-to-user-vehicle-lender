from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.vehicles.mixins import VehicleOwnerMixing
from apps.vehicles.models import Vehicle


class CreateVehicleView(LoginRequiredMixin, generic.CreateView):
    queryset = Vehicle.objects.select_related("owner").all()
    template_name = "vehicles/create.html"

    def form_valid(self, form):
        form.owner = self.request.user
        messages.success(self.request, f"vehicle {form.type} added successfully.")
        return super().form_valid(form)


class ListVehicleView(LoginRequiredMixin, VehicleOwnerMixing, generic.ListView):
    queryset = Vehicle.objects.select_related("owner").all()
    template_name = "vehicles/list.html"
    context_object_name = "vehicles"
    paginate_by = 20

    def get_queryset(self):
        return self.queryset.filter(location=self.request.user.location)


class SearchVehicleView(generic.TemplateView):
    template_name = "vehicles/search.html"


class SearchResultView(generic.ListView):
    queryset = Vehicle.objects.select_related("owner").filter(availability_status=True).all()
    template_name = "vehicles/search_results.html"
    context_object_name = "vehicles"
    paginate_by = 20

    def get_queryset(self):
        vehicle_type: str = self.query_params.get("type")
        location: str = self.query_params.get("location")
        if (vehicle_type is not None or vehicle_type != " ") or (location is not None or location != " "):
            qs = Q(type__icontains=vehicle_type) | Q(location__icontains=location)
            return self.queryset.filter(qs)
        return self.queryset.filter(location__icontains=self.request.user.location)
