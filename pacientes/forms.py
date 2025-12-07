# -------------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Archivo: softmedic/pacientes/forms.py
# Versión: 1.0
# Fecha: 13/11/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# -------------------------------------------------------------------
"""
Formularios del módulo de pacientes.
Incluye formulario principal para registro y edición de pacientes.
"""
# ------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Archivo: pacientes/forms.py
# Versión: 1.1
# Fecha: 23/11/2025
# Elaborado por: Prixma Software Projects
# ------------------------------------------------------------

from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    """
    Formulario para creación y edición de pacientes.
    Se ajusta correctamente al modelo Paciente con relación a EPS.
    """

    class Meta:
        model = Paciente
        fields = [
            'nombre_completo',
            'identificacion',
            'fecha_nacimiento',
            'contacto',
            'eps'
        ]

        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono o correo'
            }),
            'eps': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
