# users/context_processors.py

def user_role(request):
    role = None
    if request.user.is_authenticated:
        try:
            role = request.user.userprofile.role
        except Exception:
            role = None
    return {'user_role': role}
