# archivo: softmedic/pacientes/models.py
# ------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Versión: 1.1
# Fecha: 09/11/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# ------------------------------------------------------------
# Descripción: Definición de los modelos de datos "Paciente" y
# "EPS", junto con su formulario asociado para la gestión y 
# validación de información.
# ------------------------------------------------------------

from django.db import models
from django import forms
from datetime import date

# ============================================================
# MODELO: EPS (Entidad Promotora de Salud)
# ============================================================

class EPS(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="EPS / Aseguradora")
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código EPS")
    contacto = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Correo de contacto")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        db_table = "eps"
        ordering = ["nombre"]
        verbose_name = "EPS"
        verbose_name_plural = "EPS / Aseguradoras"

    def __str__(self):
        return self.nombre


# ============================================================
# MODELO: Paciente
# ============================================================

class Paciente(models.Model):
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre completo")
    identificacion = models.CharField(max_length=20, unique=True, verbose_name="Identificación")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    contacto = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contacto (teléfono o email)")
    eps = models.ForeignKey(EPS, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="EPS / Aseguradora de salud")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        db_table = "paciente"
        ordering = ["nombre_completo"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return f"{self.nombre_completo} ({self.identificacion})"


# ============================================================
# FORMULARIO: PacienteForm
# ============================================================

class PacienteForm(forms.ModelForm):
    """
    Formulario basado en el modelo Paciente.
    Incluye validaciones de edad y formato de fecha de nacimiento.
    """

    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'placeholder': 'Nombre y apellidos'}),
            'identificacion': forms.TextInput(attrs={'placeholder': 'Número de identificación'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'contacto': forms.TextInput(attrs={'placeholder': 'Teléfono o correo electrónico'}),
            'eps': forms.Select(),
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        edad = (date.today() - fecha).days // 365

        if edad < 0:
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        if edad > 120:
            raise forms.ValidationError("Edad no válida (mayor a 120 años).")

        return fecha


# ============================================================
# CONTROL DE VERSIONAMIENTO
# ============================================================

# | Versión | Fecha       | Autor / Responsable                        | Descripción de cambios |
# |----------|-------------|--------------------------------------------|------------------------|
# | 1.0      | 03/11/2025  | Equipo de Arquitectura y Análisis Técnico Soft-Medic | Consolidación y validación del diseño técnico completo del sistema. |
# | 1.1      | 09/11/2025  | Equipo de Arquitectura y Análisis Técnico Soft-Medic | Integración del modelo "EPS" y relación foránea en el modelo "Paciente". |
