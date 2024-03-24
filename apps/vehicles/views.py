import mimetypes
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.common.utils import Validators
from apps.vehicles.mixins import VehicleOwnerMixing
from apps.vehicles.models import Vehicle
from django.shortcuts import redirect
from core.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage


class CreateVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Vehicle
    fields = "__all__"
    template_name = "vehicles/create.html"

    def post(self, request, *args, **kwargs):
        allowed_content_types = ["image/jpg", "image/jpeg", "image/png"]
        user_data: dict = {
            "owner": request.user,
            "type": request.POST.get("type"),
            "make": request.POST.get("make"),
            "model": request.POST.get("model"),
            "year": request.POST.get("year"),
            "max_speed": request.POST.get("max_speed"),
            "total_doors": request.POST.get("total_doors"),
            "transmission_types": request.POST.get("transmission_types"),
            "total_passenger": request.POST.get("total_passenger"),
            "registration_number": request.POST.get("registration_number"),
            "fuel_type": request.POST.get("fuel_type"),
            "aircondition": request.POST.get("aircondition"),
            "engine_capacity": request.POST.get("engine_capacity"),
            "availability_status": request.POST.get("availability_status"),
            "price_per_hours": request.POST.get("price_per_hours"),
            "pickup_location": request.POST.get("pickup_location"),
            "image": request.FILES.get("image"),
            "description": request.POST.get("description"),
        }

        image = user_data.get("image")

        if not image:
            messages.error(
                request, f"Please upload your identification document.")
            return redirect("create_user")

        if image.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            messages.warning(
                request, f"Document cannot be larger than {Validators.convert_to_megabyte(image.file_size)}MB.")
            return redirect("create_user")

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_type = mimetypes.guess_type(filename)[0]

        if file_type not in allowed_content_types:
            messages.info(
                request, "invalid file  upload, only png, jpg, jpeg file types are accepted.")
            return redirect('create_user')


class ListVehicleView(LoginRequiredMixin, VehicleOwnerMixing, generic.ListView):
    queryset = Vehicle.objects.select_related("owner").all()
    template_name = "vehicles/list.html.html"
    context_object_name = "vehicles"
    paginate_by = 20


class VehicleDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Vehicle.objects.select_related("owner").all()
    template_name = "vehicles/detail.html"
    context_object_name = "vehicle"
    success_url = reverse_lazy("book_vehicle")
