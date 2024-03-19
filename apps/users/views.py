from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import UserForm, UserUpdateForm
from apps.common.utils import Validators


class RegisterUserView(generic.CreateView):
    queryset = CustomUser.objects.all()
    form_class = UserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("user_login")

    def form_valid(self, request, form):
        if not self.validate_email(form.instance.email):
            messages.error(self.request, "email already exist.")
            return redirect("create_user")

        if not Validators.validate_file_size(form.instance.document):
            messages.error(
                self.request, "invalid file  upload, only pdf, png, jpg, jpeg file types are accepted.")
            return redirect("create_user")

        messages.success(self.request, "registration successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "an error occured, please try again.")
        return super().form_invalid(form)

    def validate_email(self, email):
        if self.queryset.filter(email=email).exists():
            return False
        return True


class ListUserView(LoginRequiredMixin, generic.ListView):
    queryset = CustomUser.objects.all()
    template_name = "users/list.html"
    context_object_name = "users"
    success_url = reverse_lazy("user_login")
    paginated_by = 20


class RetrieveUserView(LoginRequiredMixin, generic.DetailView):
    queryset = CustomUser.objects.all()
    template_name = "users/rerieve.html"
    context_object_name = "user"
    success_url = reverse_lazy("user_login")


class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    queryset = CustomUser.objects.all()
    template_name = "users/update.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("user_login")

    def form_valid(self, request, form):
        messages.success(self.request, "profile update successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "could not update profile, please try again.")
        return super().form_invalid(form)


class DeleteUserView(LoginRequiredMixin, generic.DeleteView):
    queryset = CustomUser.objects.all()
    template_name = "users/delete.html"
    success_url = reverse_lazy("user_login")


class UserLoginView(generic.TemplateView):
    template_name = "users/login.html"
    success_url = reverse_lazy('user_profile')

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect('success')
        return redirect("user_login")

    def form_valid(self, request, form):
        messages.success(self.request, "login successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "login unsuccessful, please try again")
        return super().form_invalid(form)


class UserLogoutView(generic.TemplateView):
    success_url = reverse_lazy("user_login")

    def get(self, request):
        logout(request)
        return redirect('user_login')

    def form_valid(self, request, form):
        messages.success(self.request, "logout successful.")
        return super().form_valid(form)


class CustomChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    queryset = CustomUser.objects.all()
    template_name = 'users/password_change.html'
    success_url = reverse_lazy("update_user")

    def form_valid(self, request, form):
        messages.success(self.request, "password reset successful.")
        return super().form_valid(form)

    def form_invalid(self, request, form):
        messages.error(request, "could not reset password, please try again.")
        return super().form_invalid(form)


class CustomPasswordResetCompleteView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_complete.html'
