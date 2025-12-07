# =============================================================================
# Proyecto: SOFT-MEDIC
# Archivo: historias/views.py
# Versión: 4.0
# Fecha: 05/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# =============================================================================

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import HistoriaClinica
from .forms import (
    HistoriaClinicaForm,
    DiagnosticoFormSet,
    MedicamentoFormSet,
    ObservacionFormSet,
    HistoriaAdjuntoFormSet
)

from .permisos import (
    puede_ver_historia,
    puede_editar_historia,
    puede_eliminar_historia
)


# ---------------------------------------------------------------------------
# LISTAR HISTORIAS
# ---------------------------------------------------------------------------
class HistoriaClinicaListView(LoginRequiredMixin, ListView):
    model = HistoriaClinica
    template_name = 'historias/historia_list.html'
    context_object_name = 'historias'

    def get_queryset(self):
        user = self.request.user

        if user.rol == 'MEDICO':
            return HistoriaClinica.objects.filter(medico_responsable=user)

        if user.rol in ['RECEPCIONISTA', 'ADMIN']:
            return HistoriaClinica.objects.all()

        return HistoriaClinica.objects.none()


# ---------------------------------------------------------------------------
# CREAR HISTORIA - SOLO MÉDICO
# ---------------------------------------------------------------------------
class HistoriaClinicaCreateView(LoginRequiredMixin, CreateView):
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historias/editar_hce.html'
    success_url = reverse_lazy('historias:listar_historias')

    def dispatch(self, request, *args, **kwargs):
        if request.user.rol != 'MEDICO':
            return HttpResponseForbidden("Solo un médico puede crear historias clínicas.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['diag_formset'] = DiagnosticoFormSet(self.request.POST)
            data['med_formset'] = MedicamentoFormSet(self.request.POST)
            data['obs_formset'] = ObservacionFormSet(self.request.POST)
            data['adj_formset'] = HistoriaAdjuntoFormSet(self.request.POST, self.request.FILES)
        else:
            data['diag_formset'] = DiagnosticoFormSet()
            data['med_formset'] = MedicamentoFormSet()
            data['obs_formset'] = ObservacionFormSet()
            data['adj_formset'] = HistoriaAdjuntoFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        diag_formset = context['diag_formset']
        med_formset = context['med_formset']
        obs_formset = context['obs_formset']
        adj_formset = context['adj_formset']

        if not (diag_formset.is_valid() and med_formset.is_valid() and obs_formset.is_valid() and adj_formset.is_valid()):
            messages.error(self.request, "⚠ Revisa los datos. Algunos campos no son válidos.")
            return self.form_invalid(form)

        self.object = form.save()

        diag_formset.instance = self.object
        med_formset.instance = self.object
        obs_formset.instance = self.object
        adj_formset.instance = self.object

        diag_formset.save()
        med_formset.save()
        obs_formset.save()
        adj_formset.save()

        messages.success(self.request, "✅ Historia clínica creada correctamente.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# EDITAR HISTORIA - SOLO MÉDICO PROPIETARIO
# ---------------------------------------------------------------------------
class HistoriaClinicaUpdateView(LoginRequiredMixin, UpdateView):
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historias/editar_hce.html'
    success_url = reverse_lazy('historias:listar_historias')

    def dispatch(self, request, *args, **kwargs):
        historia = self.get_object()

        if not puede_editar_historia(request.user, historia):
            return HttpResponseForbidden("No tienes permisos para editar esta historia clínica.")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['diag_formset'] = DiagnosticoFormSet(self.request.POST, instance=self.object)
            data['med_formset'] = MedicamentoFormSet(self.request.POST, instance=self.object)
            data['obs_formset'] = ObservacionFormSet(self.request.POST, instance=self.object)
            data['adj_formset'] = HistoriaAdjuntoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['diag_formset'] = DiagnosticoFormSet(instance=self.object)
            data['med_formset'] = MedicamentoFormSet(instance=self.object)
            data['obs_formset'] = ObservacionFormSet(instance=self.object)
            data['adj_formset'] = HistoriaAdjuntoFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        diag_formset = context['diag_formset']
        med_formset = context['med_formset']
        obs_formset = context['obs_formset']
        adj_formset = context['adj_formset']

        if not (diag_formset.is_valid() and med_formset.is_valid() and obs_formset.is_valid() and adj_formset.is_valid()):
            messages.error(self.request, "⚠ Revisa los datos ingresados.")
            return self.form_invalid(form)

        self.object = form.save()

        diag_formset.instance = self.object
        med_formset.instance = self.object
        obs_formset.instance = self.object
        adj_formset.instance = self.object

        diag_formset.save()
        med_formset.save()
        obs_formset.save()
        adj_formset.save()

        messages.success(self.request, "✅ Historia clínica actualizada correctamente.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# DETALLE
# ---------------------------------------------------------------------------
class HistoriaClinicaDetailView(LoginRequiredMixin, DetailView):
    model = HistoriaClinica
    template_name = 'historias/historia_detail.html'
    context_object_name = 'historia'

    def dispatch(self, request, *args, **kwargs):
        historia = self.get_object()

        if not puede_ver_historia(request.user, historia):
            return HttpResponseForbidden("No tienes permiso para ver esta historia clínica.")

        return super().dispatch(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# ELIMINAR HISTORIA CLÍNICA – SOLO ADMIN
# ---------------------------------------------------------------------------
class HistoriaClinicaDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        historia = HistoriaClinica.objects.get(pk=kwargs['pk'])

        if not puede_eliminar_historia(request.user):
            return HttpResponseForbidden("No tienes permiso para eliminar historias clínicas.")

        tiene_diag = historia.diagnosticos_rel.exists()
        tiene_med = historia.medicamentos_rel.exists()
        tiene_obs = historia.observaciones.exists()
        tiene_citas = historia.citas.exists()
        tiene_adj = historia.adjuntos.exists()

        if any([tiene_diag, tiene_med, tiene_obs, tiene_citas, tiene_adj]):
            messages.error(
                request,
                "❌ No se puede eliminar la Historia Clínica porque tiene datos asociados."
            )
            return redirect('historias:ver_historia', pk=historia.pk)

        historia.delete()
        messages.success(request, "🗑 Historia clínica eliminada correctamente.")
        return redirect('historias:listar_historias')


# =============================================================================
# CONTROL DE CAMBIOS
# 4.0 | 05/12/2025 | PS Projects | Reescritura completa de permisos + arquitectura centralizada
# =============================================================================
