from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN'

def is_medico(user):
    return user.is_authenticated and user.rol == 'MEDICO'

def is_recepcionista(user):
    return user.is_authenticated and user.rol == 'RECEPCIONISTA'

# Decoradores personalizados
def admin_only(view_func):
    decorator = user_passes_test(is_admin, login_url='login')
    return decorator(view_func)

def medico_only(view_func):
    decorator = user_passes_test(is_medico, login_url='login')
    return decorator(view_func)

def recepcionista_only(view_func):
    decorator = user_passes_test(is_recepcionista, login_url='login')
    return decorator(view_func)
