# -------------------------------------------------------------------
# APLICACIÓN: USERS
# Archivo de rutas para la gestión de usuarios, autenticación
# y dashboards según rol (Administrador, Médico, Recepcionista).
# -------------------------------------------------------------------

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # -------------------------------------------------------------------
    # AUTENTICACIÓN
    # -------------------------------------------------------------------
    path('register/', views.register_user, name='register'),   # Registro de nuevos usuarios
    path('login/', views.login_user, name='login'),            # Inicio de sesión
    path('logout/', views.logout_user, name='logout'),         # Cierre de sesión

    # -------------------------------------------------------------------
    # DASHBOARDS SEGÚN ROL
    # -------------------------------------------------------------------
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medico_dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('recepcionista_dashboard/', views.recepcionista_dashboard, name='recepcionista_dashboard'),
    path('acceso_denegado/', views.acceso_denegado, name='acceso_denegado'),

    # -------------------------------------------------------------------
    # REPORTES DEL SISTEMA (logs de auditoría)
    # -------------------------------------------------------------------
    path('reportes/', views.reportes_sistema, name='reportes_sistema'),  # 👈 AGREGA ESTA LÍNEA

    # -------------------------------------------------------------------
    # RECUPERACIÓN DE CONTRASEÑA
    # -------------------------------------------------------------------
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/users/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
