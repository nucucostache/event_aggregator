from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def organizer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # sau URL-ul tău de login
        try:
            if request.user.userprofile.role != 'organizer':
                raise PermissionDenied
        except Exception:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            if request.user.userprofile.role != 'user':
                raise PermissionDenied
        except Exception:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


# Ce face fiecare decorator?
# Verifică dacă utilizatorul este autentificat, altfel îl trimite la login

# Verifică dacă rolul din profil este cel așteptat

# Dacă nu, aruncă o excepție PermissionDenied (pagina 403)

