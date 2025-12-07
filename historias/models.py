# Proyecto: SOFT-MEDIC
# Archivo: historia/models.py
# Versión: 1.2
# Fecha: 04/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
#
# Nota: Archivo unificado y corregido. Se ajustó el related_name del modelo
# Medicamento para evitar conflicto con el campo 'medicamentos' de HistoriaClinica.
# ---------------------------------------------------------------------

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

# Para compatibilidad con distintas versiones de Django,
# usamos models.JSONField si está disponible (Django >= 3.1).
try:
    JSONField = models.JSONField
except AttributeError:
    from django.contrib.postgres.fields import JSONField  # type: ignore

from pacientes.models import Paciente


# ============================================================
# MODELO: Historia Clínica (UNIFICADO)
# ============================================================
class HistoriaClinica(models.Model):
    # -------------------------
    # Información del Prestador
    # -------------------------
    codigo_prestador = models.CharField("Código del Prestador", max_length=50, blank=True, null=True)
    nit_prestador = models.CharField("NIT", max_length=50, blank=True, null=True)
    direccion_prestador = models.CharField("Dirección", max_length=255, blank=True, null=True)
    telefono_prestador = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    web_prestador = models.URLField("Web", blank=True, null=True)
    email_prestador = models.EmailField("Email", blank=True, null=True)

    # -------------------------
    # Datos del Paciente
    # -------------------------
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='historias_clinicas'
    )

    # -------------------------
    # Fechas administrativas
    # -------------------------
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_ingreso = models.DateField("Fecha de Ingreso", default=timezone.now)
    hora_ingreso = models.TimeField("Hora de Ingreso", auto_now_add=True)
    fecha_cierre = models.DateField("Fecha Cierre HC", blank=True, null=True)

    # -------------------------
    # Identificación y tipo
    # -------------------------
    numero_historia = models.CharField(
        "Nro. Historia",
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    tipo_historia = models.CharField("Tipo de Historia", max_length=50, blank=True, null=True)

    usuario_registra = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='historias_registradas',
        blank=True,
        null=True
    )

    # -------------------------
    # Datos Clínicos principales
    # -------------------------
    medico_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='historias_clinicas_medico'
    )
    motivo_consulta = models.TextField("Motivo de Consulta", blank=True, null=True)
    puerta_entrada = models.CharField("Puerta de Entrada / Ruta Prediagnóstica", max_length=255, blank=True, null=True)
    resumen_clinico = models.TextField("Resumen Clínico", blank=True, null=True)
    notas_adicionales = models.TextField("Notas Adicionales", blank=True, null=True)

    # =========================================================
    # SECCIÓN CLÍNICA (ENFERMEDAD ACTUAL / SÍNTOMAS)
    # =========================================================
    tiempo_evolucion = models.CharField("Tiempo de evolución", max_length=128, blank=True, null=True)
    sintomas_principales = models.TextField("Síntomas principales", blank=True, null=True)
    tratamiento_previo = models.TextField("Tratamiento previo", blank=True, null=True)

    revision_sistemas = JSONField("Revisión por sistemas", blank=True, null=True)

    # Signos vitales
    fc = models.PositiveIntegerField("Frecuencia cardiaca (FC)", null=True, blank=True)
    fr = models.PositiveIntegerField("Frecuencia respiratoria (FR)", null=True, blank=True)
    ta_sist = models.CharField("TA sistólica/diastólica", max_length=16, blank=True, null=True)
    temperatura = models.DecimalField("Temperatura (°C)", max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion = models.DecimalField("Saturación (%)", max_digits=5, decimal_places=2, null=True, blank=True)
    peso = models.DecimalField("Peso (kg)", max_digits=6, decimal_places=2, null=True, blank=True)
    talla = models.DecimalField("Talla (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    imc = models.DecimalField("IMC", max_digits=5, decimal_places=2, null=True, blank=True)

    examen_fisico = models.TextField("Examen físico", blank=True, null=True)

    diagnosticos = JSONField("Diagnósticos (CIE-10)", blank=True, null=True)

    plan_manejo = models.TextField("Plan de manejo", blank=True, null=True)

    # NOTA: este campo se deja tal cual, para texto libre.
    medicamentos = models.TextField("Medicamentos / Prescripción", blank=True, null=True)

    recomendaciones = models.TextField("Recomendaciones", blank=True, null=True)

    # -------------------------
    # Auditoría
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fecha_impresion = models.DateTimeField("Fecha de Impresión", default=timezone.now)

    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"

    def __str__(self):
        try:
            paciente_str = getattr(self.paciente, 'nombre_completo', str(self.paciente))
        except Exception:
            paciente_str = "Paciente"
        numero = self.numero_historia or str(self.id)
        return f"HCE {numero} - {paciente_str}"

    # Validación: 1 historia por paciente
    def clean(self):
        if self.paciente and HistoriaClinica.objects.filter(paciente=self.paciente).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"El paciente {getattr(self.paciente, 'nombre_completo', str(self.paciente))} ya tiene una historia clínica."
            )

    # Cálculo de IMC
    def save(self, *args, **kwargs):
        try:
            if self.peso and self.talla and float(self.talla) > 0:
                self.imc = round(float(self.peso) / ((float(self.talla) / 100) ** 2), 2)
        except Exception:
            pass
        super().save(*args, **kwargs)

    # Impedir eliminación si hay dependencias
    def delete(self, using=None, keep_parents=False):
        dependencias = []

        for campo in ["diagnosticos_rel", "medicamentos_rel", "observaciones", "citas", "adjuntos"]:
            try:
                count = getattr(self, campo).count()
                if count > 0:
                    dependencias.append(f"{campo} ({count})")
            except Exception:
                pass

        if dependencias:
            raise ValidationError(
                "No es posible eliminar la Historia Clínica porque tiene registros asociados: "
                + ", ".join(dependencias)
            )

        super().delete(using=using, keep_parents=keep_parents)


# ============================================================
# MODELOS RELACIONADOS CORREGIDOS
# ============================================================
class Medicamento(models.Model):
    nombre = models.CharField(max_length=200)
    
    # 🔥 RELATED_NAME CORREGIDO
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name="medicamentos_rel"
    )

    def __str__(self):
        return self.nombre


class Diagnostico(models.Model):
    descripcion = models.CharField(max_length=255)
    codigo_cie10 = models.CharField("CIE-10", max_length=32, blank=True, null=True)
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name="diagnosticos_rel"
    )

    def __str__(self):
        return f"{self.descripcion} ({self.codigo_cie10 or 'sin código'})"


class Observacion(models.Model):
    detalle = models.TextField()
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name="observaciones"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Obs. {self.id}"


class Cita(models.Model):
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    fecha = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=50, default="PROGRAMADA")

    def __str__(self):
        try:
            paciente_str = getattr(self.historia.paciente, 'nombre_completo', str(self.historia.paciente))
        except Exception:
            paciente_str = "Paciente"
        return f"Cita {self.id} - {paciente_str}"


class HistoriaAdjunto(models.Model):
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE,
        related_name='adjuntos'
    )
    archivo = models.FileField(upload_to='historias/adjuntos/%Y/%m/%d/')
    descripcion = models.CharField(max_length=255, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjunto {self.archivo.name} ({self.historia})"


# ============================================================
# CONTROL DE CAMBIOS
# ============================================================
# Versión | Fecha       | Autor / Responsable           | Descripción
# 1.1     | 04/12/2025  | Prixma Software Projects       | Unificación Modelo HCE + secciones clínicas
# 1.2     | 04/12/2025  | Prixma Software Projects       | Corrección de conflicto related_name 'medicamentos'
