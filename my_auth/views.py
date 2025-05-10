from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "my_auth/login/page.html")

    def post(self, request):
        data = request.POST.dict()

        username = data.get("username")
        password = data.get("password")
        remember_me = data.get("remember")
        next_url = request.POST.get("next", request.GET.get("next", "chat"))

        authenticate_user = authenticate(request, username=username, password=password)

        if authenticate_user is None:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")
        else:
            login(request, authenticate_user)

            # Set session expiry based on remember me checkbox
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            else:
                # Session expires after 2 weeks (in seconds)
                request.session.set_expiry(1209600)

            return redirect(next_url)


class RegisterView(View):
    template_page = "my_auth/register/page.html"

    def get(self, request):
        return render(request, self.template_page)

    def post(self, request):
        data = request.POST.dict()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password_revalidation = data.get("password_revalidation")

        if password != password_revalidation:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, self.template_page, data)

        existing_user = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=email)
        ).first()

        if existing_user:
            if existing_user.username.lower() == username.lower():
                messages.error(
                    request, "Username already taken, please choose another one."
                )
            else:
                messages.error(
                    request, "Email already registered. Please choose another one."
                )

            return render(request, self.template_page, data)

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. You can now login.")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
