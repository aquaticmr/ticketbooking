from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect # Needed for manual forms

# Note: Django's built-in LoginView and LogoutView handle much of this,
# but they often expect a Form class. Since we are explicitly avoiding
# Django Forms, we'll implement the logic manually within a generic View.

@method_decorator(csrf_protect, name='dispatch') # Ensure CSRF protection for POST
class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        errors = []
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if password != password2:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        if errors:
            # Re-render template with errors and submitted data (optional, just errors for simplicity)
            return render(request, self.template_name, {'errors': errors, 'username': username})

        try:
            user = User.objects.create_user(username=username, password=password)
            # Log the user in immediately after registration (optional)
            login(request, user)
            return redirect('home') # Redirect to homepage after successful registration
        except Exception as e:
            errors.append(f"An error occurred: {e}")
            return render(request, self.template_name, {'errors': errors, 'username': username})

@method_decorator(csrf_protect, name='dispatch') # Ensure CSRF protection for POST
class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        # Redirect if already logged in
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        errors = []
        if not username or not password:
            errors.append("Please enter both username and password.")

        if errors:
             return render(request, self.template_name, {'errors': errors, 'username': username})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # A user was found, and the password matched
            login(request, user)
            # Redirect to a success page.
            next_url = request.GET.get('next') or reverse('home') # Redirect to 'next' if present, else home
            return redirect(next_url)
        else:
            # No user found or password didn't match
            errors.append("Invalid username or password.")
            return render(request, self.template_name, {'errors': errors, 'username': username})


class LogoutView(View):
    def get(self, request):
        # Logout only if authenticated
        if request.user.is_authenticated:
            logout(request)
        # Redirect to the logout redirect URL (configured in settings)
        return redirect('logout_redirect') # 'logout_redirect' is a dummy name, use LOGIN_REDIRECT_URL or similar

# In settings, we set LOGOUT_REDIRECT_URL. We can just redirect there directly.
# Let's simplify the LogoutView slightly.
from django.contrib.auth.views import LogoutView as DjangoLogoutView
# We can use Django's LogoutView as it doesn't use forms and handles the logout logic.
# We just need to make sure the URL name matches settings.LOGOUT_REDIRECT_URL
# For compliance, let's still use a basic View, but the logic is simple.

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        # Redirect to the page specified by LOGOUT_REDIRECT_URL in settings
        # which defaults to '/' if LOGOUT_REDIRECT_URL is not set
        return redirect(reverse('home')) # Redirect to home after logout