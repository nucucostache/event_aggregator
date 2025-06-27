from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.forms import LoginForm
from .models import UserProfile
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Salvăm rolul selectat în profilul utilizatorului
            role = form.cleaned_data.get('role')
            user.userprofile.role = role
            user.userprofile.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # 👇 Redirecționare în funcție de rol
                try:
                    role = user.userprofile.role
                    if role == 'organizer':
                        return redirect('events:dashboard_organizator')
                    else:
                        return redirect('events:event_list')  # sau orice view ai pentru useri standard
                except UserProfile.DoesNotExist:
                    messages.error(request, "Contul nu are un profil asociat.")
                    return redirect('users:login')
            else:
                messages.error(request, 'Autentificare eșuată.')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Ai fost delogat cu succes.")
    return redirect('login')

