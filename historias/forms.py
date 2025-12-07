# -------------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Archivo: softmedic/historias/forms.py
# Versión: 3.0
# Fecha: 04/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# -------------------------------------------------------------------

from django import forms
from django.forms import inlineformset_factory
from .models import (
    HistoriaClinica,
    Diagnostico,
    Medicamento,
    Observacion,
    HistoriaAdjunto
)
from users.models import CustomUser


# ================================================================
# FORM PRINCIPAL - Historia Clínica
# ================================================================
class HistoriaClinicaForm(forms.ModelForm):

    class Meta:
        model = HistoriaClinica
        fields = [
            # Datos esenciales
            'paciente',
            'motivo_consulta',
            'puerta_entrada',
            'resumen_clinico',
            'notas_adicionales',

            # Enfermedad Actual
            'tiempo_evolucion',
            'sintomas_principales',
            'tratamiento_previo',

            # Revisión por sistemas (JSON)
            'revision_sistemas',

            # Signos Vitales
            'fc', 'fr', 'ta_sist', 'temperatura', 'saturacion', 'peso', 'talla',

            # Examen Físico
            'examen_fisico',

            # Plan terapéutico
            'plan_manejo',
            'medicamentos',
            'recomendaciones',
        ]

        widgets = {
            'motivo_consulta': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'resumen_clinico': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': True}),
            'notas_adicionales': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),

            'tiempo_evolucion': forms.TextInput(attrs={'class': 'form-control'}),
            'sintomas_principales': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tratamiento_previo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),

            'revision_sistemas': forms.Textarea(attrs={'rows': 4, 'class': 'form-control',
                                                       'placeholder': 'JSON: {"respiratorio": "...", "cardiovascular": "..."}'}),

            'examen_fisico': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),

            'plan_manejo': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'medicamentos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'recomendaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    # ----------------------------------------------------------
    # Constructor con seguridad por rol (SOLO MÉDICO)
    # ----------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.user or self.user.rol != 'MEDICO':
            raise PermissionError("No tienes permiso para crear historias clínicas.")

    # ----------------------------------------------------------
    # Guardado con asignación automática del médico responsable
    # ----------------------------------------------------------
    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.medico_responsable = self.user
        instance.usuario_registra = self.user

        if commit:
            instance.save()

        return instance


# ================================================================
# FORM ADJUNTOS
# ================================================================
class HistoriaAdjuntoForm(forms.ModelForm):
    class Meta:
        model = HistoriaAdjunto
        fields = ('archivo', 'descripcion')
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


HistoriaAdjuntoFormSet = inlineformset_factory(
    HistoriaClinica,
    HistoriaAdjunto,
    form=HistoriaAdjuntoForm,
    extra=1,
    can_delete=True
)


# ================================================================
# FORMSETS DE MODELOS RELACIONADOS
# ================================================================
DiagnosticoFormSet = inlineformset_factory(
    HistoriaClinica,
    Diagnostico,
    fields=['descripcion', 'codigo_cie10'],
    extra=1,
    can_delete=True
)

MedicamentoFormSet = inlineformset_factory(
    HistoriaClinica,
    Medicamento,
    fields=['nombre'],
    extra=1,
    can_delete=True
)

ObservacionFormSet = inlineformset_factory(
    HistoriaClinica,
    Observacion,
    fields=['detalle'],
    extra=1,
    can_delete=True
)


# ================================================================
# CONTROL DE CAMBIOS
# ================================================================
# Versión | Fecha       | Autor / Responsable | Descripción
# 3.0     | 04/12/2025  | Prixma Software Projects | Unificación completa con modelo clínico ampliado + adjuntos + widgets
