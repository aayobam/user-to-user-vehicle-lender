from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.mixings import UserMixing
from .models import CustomUser
from apps.common.utils import Validators


class RegisterUserView(generic.CreateView):
    model = CustomUser
    fields = '__all__'
    template_name = "users/register.html"
    success_url = reverse_lazy("user_login")

    def post(self, request):
        user_data: dict = {
            "first_name": request.POST.get("firstName"),
            "last_name": request.POST.get("lastName"),
            "phone_no": request.POST.get("phoneNumber"),
            "document_type": request.POST.get("document_type"),
            "document": request.FILES.get("document"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password")
        }

        if not self.validate_email(user_data.get("email")):
            messages.error(self.request, "email already exist.")
            return redirect("create_user")

        if not Validators.validate_password(user_data.get("document")):
            messages.error(
                self.request, "password and confirm password do not match, please try again.")
            return redirect("create_user")

        if not Validators.validate_file_size(user_data.get("document")):
            messages.error(
                self.request, "invalid file  upload, only pdf, png, jpg, jpeg file types are accepted.")
            return redirect("create_user")

        messages.success(self.request, "registration successful.")
        return super().post(request)

    def form_invalid(self, form):
        messages.error(self.request, "an error occured, please try again.")
        return super().form_invalid(form)

    def validate_email(self, email):
        if self.queryset.filter(email=email).exists():
            return False
        return True


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    queryset = CustomUser.objects.all()
    template_name = "users/profile.html"
    context_object_name = "user"
    success_url = reverse_lazy("user_profile")

    def put(self, request, *args,  **kwargs):
        user_data: dict = {
            "first_name": request.POST.get("firstName"),
            "last_name": request.POST.get("lastName"),
            "phone_no": request.POST.get("phoneNumber"),
            "document_type": request.POST.get("document_type"),
            "document": request.FILES.get("document"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "confirm_password": request.POST.get("confirm_password")
        }

        user = self.get_object(**user_data)
        user.save()
        return super().put(request, *args, **kwargs)

    def form_valid(self, request, form):
        messages.success(self.request, "profile update successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "could not update profile, please try again.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class DeleteUserView(LoginRequiredMixin, generic.DeleteView):
    queryset = CustomUser.objects.all()
    template_name = "users/delete.html"
    success_url = reverse_lazy("user_login")


class UserLoginView(UserMixing, generic.TemplateView):
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
    success_url = reverse_lazy("user_login")

    def get(self, request):
        logout(request)
        messages.success(self.request, "logout successful.")
        return redirect('user_login')


class CustomChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    queryset = CustomUser.objects.all()
    template_name = 'users/change_password.html'
    success_url = reverse_lazy("update_user")

    def form_valid(self, request, form):
        messages.success(self.request, "password reset successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "could not reset password, please try again.")
        return super().form_invalid(form)


class ResetPasswordView(generic.TemplateView):
    template_name = 'users/reset_password.html'


class CustomPasswordResetCompleteView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_complete.html'
