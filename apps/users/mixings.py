from django.shortcuts import redirect


class UserMixing:
    def is_authenticated_user(request):
        if request.user.is_authenticated:
            return redirect("user_profile")
