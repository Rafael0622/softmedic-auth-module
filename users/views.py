# -------------------------------------------------------------------
# users/views.py
# -------------------------------------------------------------------
import os
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from .forms import CustomUserCreationForm, CustomLoginForm, PasswordResetRequestForm
from .decorators import admin_required, medico_required, recepcionista_required

User = get_user_model()
logger = logging.getLogger('users')  # Logger específico para la app 'users'


# -------------------------------------------------------------------
# REGISTRO DE USUARIO
# -------------------------------------------------------------------
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = user.nombre
            user.last_name = ''
            user.save()
            logger.info(f"REGISTRO EXITOSO: Usuario {user.correo} ({user.rol}) creado por formulario web.")
            messages.success(request, "✅ Usuario creado exitosamente.")
            return redirect('users:login')
        else:
            logger.warning("REGISTRO FALLIDO: Datos inválidos en formulario de registro.")
            messages.error(request, "⚠️ Error al registrar el usuario. Verifica los datos.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# -------------------------------------------------------------------
# LOGIN DE USUARIO
# -------------------------------------------------------------------
def login_user(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=correo, password=password)
            if user:
                login(request, user)
                request.session.set_expiry(900)
                logger.info(f"LOGIN EXITOSO: Usuario {user.correo} ({user.rol})")
                messages.success(request, f"👋 Bienvenido, {user.nombre}.")
                if user.rol == 'ADMIN':
                    return redirect('users:admin_dashboard')
                elif user.rol == 'MEDICO':
                    return redirect('users:medico_dashboard')
                elif user.rol == 'RECEPCIONISTA':
                    return redirect('users:recepcionista_dashboard')
                else:
                    logger.warning(f"LOGIN SIN ROL ASIGNADO: Usuario {user.correo}")
                    messages.warning(request, "Rol no asignado. Contacte al administrador.")
                    return redirect('users:login')
            else:
                logger.warning(f"LOGIN FALLIDO: Intento de acceso con {correo}")
                messages.error(request, "❌ Credenciales inválidas.")
        else:
            logger.warning("LOGIN FALLIDO: Formulario de autenticación inválido.")
            messages.error(request, "⚠️ Error en el formulario de autenticación.")
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})


# -------------------------------------------------------------------
# LOGOUT DE USUARIO
# -------------------------------------------------------------------
@login_required
def logout_user(request):
    logger.info(f"LOGOUT: Usuario {request.user.correo} ({request.user.rol}) cerró sesión.")
    logout(request)
    messages.info(request, "👋 Sesión cerrada correctamente.")
    return redirect('users:login')


# -------------------------------------------------------------------
# DASHBOARDS POR ROL
# -------------------------------------------------------------------
@login_required
@admin_required
def admin_dashboard(request):
    logger.info(f"ACCESO: {request.user.correo} ingresó al panel ADMIN.")
    return render(request, 'users/admin_dashboard.html')


@login_required
@medico_required
def medico_dashboard(request):
    """
    Panel principal del médico.
    Acceso libre dentro del módulo clínico (sin restricciones internas).
    """
    logger.info(f"ACCESO: {request.user.correo} ingresó al panel MÉDICO (sin restricciones).")
    context = {
        'usuario': request.user,
        'titulo_panel': "Panel del Médico",
        'descripcion': "Acceso completo al módulo clínico del sistema.",
    }
    return render(request, 'users/medico_dashboard.html', context)


@login_required
@recepcionista_required
def recepcionista_dashboard(request):
    logger.info(f"ACCESO: {request.user.correo} ingresó al panel RECEPCIONISTA.")
    return render(request, 'users/recepcionista_dashboard.html')


# -------------------------------------------------------------------
# ACCESO DENEGADO
# -------------------------------------------------------------------
@login_required
def acceso_denegado(request):
    logger.warning(f"ACCESO DENEGADO: {request.user.correo} intentó acceder a un recurso restringido.")
    return render(request, 'users/acceso_denegado.html', status=403)


# -------------------------------------------------------------------
# RECUPERACIÓN DE CONTRASEÑA
# -------------------------------------------------------------------
@csrf_protect
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            try:
                user = User.objects.get(correo=correo)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                message = render_to_string('users/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url
                })
                send_mail(
                    'Recuperación de contraseña Soft-Medic',
                    message,
                    None,
                    [correo],
                    fail_silently=False,
                )
                logger.info(f"SOLICITUD DE RECUPERACIÓN DE CONTRASEÑA: Enviada a {correo}")
            except User.DoesNotExist:
                logger.warning(f"RECUPERACIÓN FALLIDA: No existe usuario con correo {correo}")
            return redirect('users:password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_form.html', {'form': form})


# -------------------------------------------------------------------
# REPORTES DEL SISTEMA (solo ADMIN)
# -------------------------------------------------------------------
@login_required
@user_passes_test(lambda u: u.rol == 'ADMIN')
def reportes_sistema(request):
    """Muestra los contenidos de los archivos de logs del sistema con manejo de codificación segura."""
    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    logs_content = ""

    log_files = [
        ('users.log', '📘 Actividades de Usuarios'),
        ('security.log', '🛡️ Seguridad y Accesos'),
        ('audit.log', '📋 Auditoría del Sistema'),
        ('errors.log', '❌ Errores del Sistema'),
    ]

    for filename, title in log_files:
        file_path = os.path.join(log_dir, filename)
        if os.path.exists(file_path):
            try:
                # Intentar primero UTF-8
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip() or "Sin registros disponibles."
            except UnicodeDecodeError:
                # Si falla, intentar Latin-1
                with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
                    content = f.read().strip() or "Sin registros disponibles (codificación incompatible)."
            logs_content += f"\n\n===== {title} ({filename}) =====\n{content}\n"
        else:
            logs_content += f"\n\n===== {title} ({filename}) =====\nArchivo no encontrado.\n"

    logger.info(f"ACCESO: {request.user.correo} ingresó a la sección de REPORTES DEL SISTEMA.")
    return render(request, 'users/reportes_sistema.html', {'logs_content': logs_content})
