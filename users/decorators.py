from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """Restringe el acceso solo a usuarios con rol ADMIN."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "⚠️ Debes iniciar sesión para acceder.")
            return redirect('users:login')

        if hasattr(request.user, 'rol') and request.user.rol == 'ADMIN':
            return view_func(request, *args, **kwargs)

        messages.error(request, "⛔ Acceso denegado: Solo para administradores.")
        return redirect('users:acceso_denegado')
    return wrapper


def medico_required(view_func):
    """Restringe el acceso solo a usuarios con rol MEDICO."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "⚠️ Debes iniciar sesión para acceder.")
            return redirect('users:login')

        if hasattr(request.user, 'rol') and request.user.rol == 'MEDICO':
            return view_func(request, *args, **kwargs)

        messages.error(request, "⛔ Acceso denegado: Solo para médicos.")
        return redirect('users:acceso_denegado')
    return wrapper


def recepcionista_required(view_func):
    """Restringe el acceso solo a usuarios con rol RECEPCIONISTA."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "⚠️ Debes iniciar sesión para acceder.")
            return redirect('users:login')

        if hasattr(request.user, 'rol') and request.user.rol == 'RECEPCIONISTA':
            return view_func(request, *args, **kwargs)

        messages.error(request, "⛔ Acceso denegado: Solo para recepcionistas.")
        return redirect('users:acceso_denegado')
    return wrapper
