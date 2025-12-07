# -------------------------------------------------------------------
# softmedic/urls.py
# -------------------------------------------------------------------
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# -------------------------------------------------------------------
# VISTA RAÍZ — REDIRECCIÓN SEGÚN ROL O LOGIN
# -------------------------------------------------------------------
def root_redirect(request):
    """Redirige al dashboard correspondiente según el rol del usuario,
    o al login si no está autenticado.
    """
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'rol'):
            if user.rol == 'ADMIN':
                return redirect('users:admin_dashboard')
            elif user.rol == 'MEDICO':
                return redirect('users:medico_dashboard')
            elif user.rol == 'RECEPCIONISTA':
                return redirect('users:recepcionista_dashboard')
        # Si el usuario autenticado no tiene rol asignado
        return redirect('users:login')
    # Usuario no autenticado → al login
    return redirect('users:login')

# -------------------------------------------------------------------
# URL PATTERNS PRINCIPALES DEL PROYECTO
# -------------------------------------------------------------------
urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Rutas del módulo "users"
    path('users/', include('users.urls')),

    # Rutas del módulo "pacientes"
    path('pacientes/', include(('pacientes.urls', 'pacientes'), namespace='pacientes')),

    # RUTAS DEL MÓDULO "historias"
    path('historias/', include(('historias.urls', 'historias'), namespace='historias')),

    # -------------------------------------------------------------------
    # Recuperación de contraseña
    # -------------------------------------------------------------------
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='/password_reset/done/'
         ), name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/reset/done/'
         ), name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), name='password_reset_complete'),

    # Ruta raíz → redirección automática según selección por rol o login
    path('', root_redirect, name='root_redirect'),
]

# -------------------------------------------------------------------
# SERVIR ARCHIVOS ESTÁTICOS Y MEDIA EN DESARROLLO
# -------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# -------------------------------------------------------------------
# ACCESO RÁPIDO A DASHBOARDS (para referencia)
# -------------------------------------------------------------------
# ADMIN: http://127.0.0.1:8000/users/admin_dashboard/
# MÉDICO: http://127.0.0.1:8000/users/medico_dashboard/
# RECEPCIONISTA: http://127.0.0.1:8000/users/recepcionista_dashboard/
