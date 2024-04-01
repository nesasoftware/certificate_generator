from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users_temp/registration.html', {'form': form})



class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Your username must be unique and can contain up to 150 characters. Only letters, digits, and @/./+/-/_ characters are allowed."




def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('index')
            else:
                # Authentication failed, return an error message
                error_message = "Invalid username or password"
                return render(request, 'users_temp/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    # Render the login page with the login form
    return render(request, 'users_temp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    # Redirect to a desired page after logout
    return redirect('login')