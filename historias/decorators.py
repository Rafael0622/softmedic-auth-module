# =====================================================================
# Proyecto: SOFT-MEDIC
# Archivo: historias/decorators.py
# Versión: 1.0
# Fecha: 05/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# =====================================================================

from functools import wraps
from django.http import HttpResponseForbidden


# ---------------------------------------------------------------
# Utilidad base
# ---------------------------------------------------------------
def rol_requerido(roles_permitidos):
    """
    Decorador genérico que verifica si el usuario tiene un rol permitido.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("Debes iniciar sesión.")

            # Seguridad: si no tiene atributo rol, no puede acceder
            rol_usuario = getattr(user, "rol", None)

            if rol_usuario not in roles_permitidos:
                return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


# ---------------------------------------------------------------
# Decoradores especializados
# ---------------------------------------------------------------
def medico_required(view_func):
    return rol_requerido(["MEDICO"])(view_func)


def admin_required(view_func):
    return rol_requerido(["ADMIN"])(view_func)


def medico_o_admin(view_func):
    return rol_requerido(["MEDICO", "ADMIN"])(view_func)
