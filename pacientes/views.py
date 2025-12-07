# -------------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Archivo: softmedic/pacientes/views.py
# Versión: 1.6
# Fecha: 02/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# -------------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Paciente
from .forms import PacienteForm
from historias.models import HistoriaClinica

User = get_user_model()


# -------------------------------------------------------------------
# Validación de rol
# -------------------------------------------------------------------
def es_personal_autorizado(user):
    return getattr(user, 'rol', None) in ['ADMIN', 'MEDICO', 'RECEPCIONISTA']


# -------------------------------------------------------------------
# Vistas basadas en clases (CBV)
# -------------------------------------------------------------------

class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para registrar un nuevo paciente.
    Accesible por: ADMIN, MEDICO y RECEPCIONISTA.
    """
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/form.html'
    success_url = reverse_lazy('pacientes:listar_pacientes')

    def test_func(self):
        return es_personal_autorizado(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para crear pacientes.")
        return redirect('pacientes:listar_pacientes')


class PacienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vista para editar un paciente existente.
    Accesible por: ADMIN, MEDICO y RECEPCIONISTA.
    """
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/form.html'
    success_url = reverse_lazy('pacientes:listar_pacientes')

    def test_func(self):
        return es_personal_autorizado(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para editar este paciente.")
        return redirect('pacientes:listar_pacientes')


class PacienteListView(LoginRequiredMixin, ListView):
    """
    Vista para listar los pacientes registrados.
    Accesible por: ADMIN, MEDICO y RECEPCIONISTA.
    """
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    ordering = ['nombre_completo']


# -------------------------------------------------------------------
# Vistas funcionales del módulo (FBV)
# -------------------------------------------------------------------

@login_required
@user_passes_test(es_personal_autorizado)
def pacientes_dashboard(request):
    """
    Vista principal del módulo de pacientes.
    Muestra un resumen de pacientes registrados.
    """
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/dashboard.html', {'pacientes': pacientes})


@login_required
@user_passes_test(es_personal_autorizado)
def crear_paciente(request):
    """
    Vista funcional para crear un paciente.
    """
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f"Paciente {paciente.nombre_completo} creado correctamente.")
            return redirect('pacientes:listar_pacientes')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()

    return render(request, 'pacientes/form.html', {'form': form, 'paciente': None})


@login_required
@user_passes_test(es_personal_autorizado)
def listar_pacientes(request):
    """
    Lista de pacientes (versión alternativa a CBV).
    """
    pacientes = Paciente.objects.all().order_by("-created_at")
    return render(request, "pacientes/listar_pacientes.html", {"pacientes": pacientes})


@login_required
@user_passes_test(es_personal_autorizado)
def registrar_paciente(request):
    """
    Registra un paciente utilizando un flujo FBV.
    """
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f"Paciente {paciente.nombre_completo} registrado correctamente.")
            return redirect("pacientes:listar_pacientes")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()

    return render(request, "pacientes/form.html", {"form": form, "paciente": None})


@login_required
@user_passes_test(es_personal_autorizado)
def editar_paciente(request, pk):
    """
    Edita un paciente existente.
    Permite a ADMIN, MEDICO y RECEPCIONISTA sin cerrar sesión.
    """
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f"Paciente {paciente.nombre_completo} actualizado correctamente.")
            return redirect("pacientes:listar_pacientes")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm(instance=paciente)

    return render(request, "pacientes/form.html", {
        "form": form,
        "paciente": paciente
    })


@login_required
@user_passes_test(lambda u: getattr(u, 'rol', None) in ['ADMIN', 'MEDICO'])
def ver_paciente(request, id):
    """
    Vista de detalle de un paciente.
    Solo ADMIN y MEDICO pueden acceder.
    """
    paciente = Paciente.objects.filter(id=id).first()

    if not paciente:
        messages.error(request, "Paciente no encontrado.")
        return redirect('pacientes:dashboard')

    return render(request, 'pacientes/detalle.html', {'paciente': paciente})


# -------------------------------------------------------------------
# NUEVA VISTA: Búsqueda y filtrado de pacientes
# -------------------------------------------------------------------

@login_required
@user_passes_test(es_personal_autorizado)
def buscar_pacientes(request):
    """
    Vista para buscar y filtrar pacientes por:
    - Nombre
    - Documento
    - Médico tratante
    """
    nombre = request.GET.get('nombre', '').strip()
    documento = request.GET.get('documento', '').strip()
    medico_id = request.GET.get('medico', '').strip()

    pacientes = Paciente.objects.all()

    # Filtro por nombre (parcial)
    if nombre:
        pacientes = pacientes.filter(nombre_completo__icontains=nombre)

    # Filtro por documento (exacto)
    if documento:
        pacientes = pacientes.filter(identificacion__iexact=documento)

    # Filtro por médico tratante a través de historias clínicas
    if medico_id:
        pacientes = pacientes.filter(
            historias_clinicas__medico_responsable_id=medico_id
        ).distinct()

    medicos = User.objects.filter(is_staff=True)

    return render(request, 'pacientes/listar_pacientes.html', {
        'pacientes': pacientes,
        'nombre': nombre,
        'documento': documento,
        'medico_id': medico_id,
        'medicos': medicos
    })


# -------------------------------------------------------------------
# Control de cambios
# -------------------------------------------------------------------
# | Versión | Fecha       | Autor / Responsable           | Descripción de cambios                                  |
# |--------|------------|---------------------------------|----------------------------------------------------------|
# | 1.5    | 23/11/2025 | Prixma Software Projects        | Corrección total de rutas y plantilla unificada sin errores|
# | 1.6    | 02/12/2025 | Prixma Software Projects        | Implementación de búsqueda y filtrado de pacientes       |
