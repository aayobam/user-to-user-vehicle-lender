import mimetypes
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from apps.bookings.models import Booking
from core.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from apps.common import choices
from .models import CustomUser
from apps.common.utils import Validators
from .mixings import is_authenticated


@method_decorator(is_authenticated, name="dispatch")
class RegisterUserView(generic.CreateView):
    model = CustomUser
    fields = '__all__'
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        allowed_content_types = ['application/pdf',
                                 'image/jpeg', 'image/jpg', 'image/png']
        user_data = {
            "first_name": request.POST.get("firstName"),
            "last_name": request.POST.get("lastName"),
            "phone_no": request.POST.get("phoneNumber"),
            "document_type": request.POST.get("document_type"),
            "document": request.FILES.get("formFile"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }
        document = user_data.get("document")
        confirm_password = request.POST.get("confirm_password")

        email = user_data.get("email")

        if not self.validate_email(email):
            messages.error(self.request, f"email: {email} already exist.")
            return redirect("create_user")

        if not Validators.validate_password(user_data.get("password"), confirm_password):
            messages.error(self.request, "password and confirm password do not match, please try again.")
            return redirect("create_user")

        if not Validators.validate_password_length(user_data.get("password")):
            messages.error(self.request, "password lenght cannot be less than 10, please try again.")
            return redirect("create_user")

        if not document:
            messages.error(request, f"Please upload your identification document.")
            return redirect("create_user")

        if document.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            messages.warning(request, f"Document cannot be larger than {Validators.convert_to_megabyte(document.file_size)}MB.")
            return redirect("create_user")

        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        file_type = mimetypes.guess_type(filename)[0]

        if file_type not in allowed_content_types:
            messages.info(request, "invalid file  upload, only pdf, png, jpg, jpeg file types are accepted.")
            return redirect('create_user')

        user: CustomUser = self.model.objects.create(**user_data)
        user.set_password(user_data.get("password"))
        user.save()
        messages.success(self.request, "registration successful.")
        return redirect("user_login")

    def validate_email(self, email):
        if self.model.objects.filter(email=email).exists():
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["DOCUMENT_TYPES"] = choices.DOCUMENT_TYPES
        return context


class UserProfileView(LoginRequiredMixin, generic.UpdateView):
    """
    Users can view their profiles and perform updates.
    """
    model = CustomUser
    fields = ['first_name', 'last_name', 'phone_no', 'document', 'email']
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def patch_user(self, user, data):
        for key, value in data.items():
            setattr(user, key, value)
        user.save()

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = {
            "first_name": request.POST.get("firstName"),
            "last_name": request.POST.get("lastName"),
            "phone_no": request.POST.get("phoneNumber"),
            "document": request.FILES.get("formFile"),
            "email": request.POST.get("email")
        }
        self.patch_user(user, user_data)
        messages.success(request, "profile updated successfully")
        return redirect("user_profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        context["total_booking"] = Booking.objects.select_related("vehicle", "renter").filter(renter=self.request.user)
        return context


class DeleteUserView(LoginRequiredMixin, generic.DeleteView):
    """
    users can delete their profile, but this button doesn't exist on template. (optional)
    """
    queryset = CustomUser.objects.all()
    template_name = "users/delete.html"
    success_url = reverse_lazy("user_login")


@method_decorator(is_authenticated, name="dispatch")
class UserLoginView(generic.TemplateView):
    model = CustomUser
    template_name = "users/login.html"
    success_url = reverse_lazy('user_profile')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Email does not exist.")
            return redirect("user_login")

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("user_profile")

        messages.error(request, "Login unsuccessful, please try again.")
        return redirect("user_login")


class UserLogoutView(generic.TemplateView):
    def get(self, request):
        logout(request)
        messages.success(self.request, "logout successful.")
        return redirect('user_login')


class ChangePasswordView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy("user_profile")

    def post(self, request, *args, **kwargs):
        old_password: str = request.POST.get("old_password")
        new_password1: str = request.POST.get('new_password1')
        new_password2: str = request.POST.get('new_password2')

        user: CustomUser = request.user

        if not user.check_password(old_password):
            messages.warning(request, "old password doesn't match.")
            return redirect("change_password")

        if len(new_password1) < 10:
            messages.warning(request, "password length should not be less than 10.")
            return redirect("change_password")

        if old_password == new_password1:
            messages.warning(request, "your new password cannot be the same as your old password.")
            return redirect("change_password")

        if new_password1 != new_password2:
            messages.warning(request, "new_password1 and new_password2 do not match.")
            return redirect("change_password")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "password change successfull. your new password would take effect on next login.")
        return redirect("user_profile")
