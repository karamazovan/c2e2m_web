from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi{username}, your account has created successfully')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form':form})

def profile(request):
    return render(request, 'users/profile.html')