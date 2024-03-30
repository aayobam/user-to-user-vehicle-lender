import mimetypes
from django.db.models import Q
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
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
from apps.common import choices


class CreateVehicleView(LoginRequiredMixin, generic.CreateView):
    model = Vehicle
    fields = "__all__"
    template_name = "vehicles/add_vehicle.html"
    context_object_name = "vehicle"

    def post(self, request, *args, **kwargs):
        allowed_image_types = ["image/jpg", "image/jpeg", "image/png"]
        allowed_content_types = ["image/jpg",
                                 "image/jpeg", "image/png", "application/pdf"]
        vehicle_data = {
            "owner": request.user,
            'model': request.POST.get('vehicle-model'),
            'year': request.POST.get('vehicle-year'),
            'vehicle_make': request.POST.get('vehicle-make'),
            'vehicle_type': request.POST.get('vehicle-type'),
            'price_per_hour': request.POST.get('vehicle-price'),
            'pickup_location': request.POST.get('pickup-location'),
            'max_speed': request.POST.get('max-speed'),
            'engine_capacity': request.POST.get('engine-capacity'),
            'total_doors': request.POST.get('no-door'),
            'total_passengers': request.POST.get('seat-capacity'),
            'transmission_type': request.POST.get('gear-type'),
            'temperature_regulator': request.POST.get('temperature'),
            'availability_status': request.POST.get('availability-status'),
            'description': request.POST.get('description'),
        }
        vehicle_image = request.FILES.get('vehicle-image')
        vehicle_reg_cert = request.FILES.get('vehicle-reg-cert')

        # validates vehicle image
        if not vehicle_image:
            messages.error(request, f"Please upload vehicle image.")
            return redirect("add_vehicle")

        if vehicle_image.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            messages.warning(
                request, f"image cannot be larger than {Validators.convert_to_megabyte(vehicle_image.file_size)}MB.")
            return redirect("add_vehicle")

        fs = FileSystemStorage()
        filename = fs.save(vehicle_image.name, vehicle_image)
        file_type = mimetypes.guess_type(filename)[0]

        if file_type not in allowed_image_types:
            messages.info(
                request, "invalid image file  upload, only png, jpg, jpeg and pdf file types are accepted.")
            return redirect('add_vehicle')

        # validates vehicle registration certificate.
        if not vehicle_reg_cert:
            messages.error(
                request, f"Please upload your registration certificate.")
            return redirect("add_vehicle")

        if vehicle_reg_cert.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            messages.warning(
                request, f"certificate cannot be larger than {Validators.convert_to_megabyte(vehicle_reg_cert.file_size)}MB.")
            return redirect("add_vehicle")

        fs = FileSystemStorage()
        filename = fs.save(vehicle_reg_cert.name, vehicle_reg_cert)
        file_type = mimetypes.guess_type(filename)[0]

        if file_type not in allowed_content_types:
            messages.info(
                request, "invalid file  upload, only png, jpg, jpeg and pdf file types are accepted.")
            return redirect('add_vehicle')

        vehicle_data["image"] = vehicle_image
        vehicle_data["registration_certificate"] = vehicle_reg_cert
        vehicle_obj = self.model.objects.create(**vehicle_data)
        vehicle_obj.save()
        messages.success(request, "vehicle created successfully.")
        return redirect("vehicle_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["VEHICLE_MAKES"] = choices.VEHICLE_MAKES
        context["VEHICLE_TYPES"] = choices.VEHICLE_TYPES
        context["GEAR_TYPES"] = choices.TRANSMISSION_TYPES
        context["FUEL_TYPE"] = choices.FUEL_TYPE
        context["TOTAL_VEHICLE_DOORS"] = choices.TOTAL_VEHICLE_DOORS
        context["TOTAL_PASSENGERS"] = choices.TOTAL_PASSENGERS
        context["TEMPERATURE_REGULATOR"] = choices.TEMPERATURE_REGULATOR
        context["AVAILABILITY_STATUS"] = choices.AVAILABILITY_STATUS
        return context


class VehicleListView(LoginRequiredMixin, generic.ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class VehicleDetailView(generic.DetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_details.html"
    context_object_name = "vehicle"
    pk_url_kwarg = "id"


class UpdateVehicleView(LoginRequiredMixin, generic.UpdateView):
    model = Vehicle
    fields = "__all__"
    template_name = "vehicles/edit_vehicle.html"
    context_object_name = "vehicle"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("vehicle_list")

    def patch_vehicle(self, vehicle, vehicle_data):
        for key, value in vehicle_data.items():
            setattr(vehicle, key, value)
        vehicle.save()

    def post(self, request, *args, **kwargs):
        allowed_content_types = ["image/jpg", "image/jpeg", "image/png"]
        vehicle_data = {
            "owner": request.user,
            'model': request.POST.get('vehicle-model'),
            'year': request.POST.get('vehicle-year'),
            'vehicle_make': request.POST.get('vehicle-make'),
            'vehicle_type': request.POST.get('vehicle-type'),
            'price_per_hour': request.POST.get('vehicle-price'),
            'pickup_location': request.POST.get('pickup-location'),
            'max_speed': request.POST.get('max-speed'),
            'engine_capacity': request.POST.get('engine-capacity'),
            'total_doors': request.POST.get('no-door'),
            'total_passengers': request.POST.get('seat-capacity'),
            'transmission_type': request.POST.get('gear-type'),
            'temperature_regulator': request.POST.get('temperature'),
            'availability_status': request.POST.get('availability-status'),
            'description': request.POST.get('description'),
        }
        vehicle_image = request.FILES.get('vehicle-image')
        vehicle_reg_cert = request.FILES.get('vehicle-reg-cert')

        if vehicle_image:
            fs = FileSystemStorage()
            filename = fs.save(vehicle_image.name, vehicle_image)
            file_type = mimetypes.guess_type(filename)[0]

            if file_type not in allowed_content_types:
                messages.info(
                    request, "Invalid file upload, only png, jpg, jpeg file types are accepted.")
                return redirect('create_user')

            if vehicle_image.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                messages.warning(
                    request, f"Document cannot be larger than {Validators.convert_to_megabyte(vehicle_image.file_size)}MB.")
                return redirect("create_user")

            vehicle_data["image"] = vehicle_image

        if vehicle_reg_cert:
            fs = FileSystemStorage()
            filename = fs.save(vehicle_reg_cert.name, vehicle_reg_cert)
            file_type = mimetypes.guess_type(filename)[0]

            if file_type not in allowed_content_types:
                messages.info(request, "invalid file  upload, only png, jpg, jpeg and pdf file types are accepted.")
                return redirect('add_vehicle')

            if vehicle_reg_cert.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                messages.warning(request, f"certificate cannot be larger than {Validators.convert_to_megabyte(vehicle_reg_cert.file_size)}MB.")
                return redirect("add_vehicle")
            
            vehicle_data["registration_certificate"] = vehicle_reg_cert


        vehicle_obj = self.get_object()
        self.patch_vehicle(vehicle_obj, vehicle_data)
        messages.success(request, "Vehicle updated successfully.")
        return redirect("update_vehicle", vehicle_obj.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["VEHICLE_MAKES"] = choices.VEHICLE_MAKES
        context["VEHICLE_TYPES"] = choices.VEHICLE_TYPES
        context["GEAR_TYPES"] = choices.TRANSMISSION_TYPES
        context["FUEL_TYPE"] = choices.FUEL_TYPE
        context["TOTAL_VEHICLE_DOORS"] = choices.TOTAL_VEHICLE_DOORS
        context["TOTAL_PASSENGERS"] = choices.TOTAL_PASSENGERS
        context["TEMPERATURE_REGULATOR"] = choices.TEMPERATURE_REGULATOR
        context["AVAILABILITY_STATUS"] = choices.AVAILABILITY_STATUS
        context["vehicle"] = self.get_object()
        return context


class DeleteVehicleView(LoginRequiredMixin, generic.DeleteView):
    model = Vehicle
    context_object_name = "vehicle"
    pk_url_kwarg = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        vehicle = self.get_object()
        vehicle.delete()
        messages.success(request, f"{vehicle.model} deleted successfully")
        return redirect("vehicle_list")
