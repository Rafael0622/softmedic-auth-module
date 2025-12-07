from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
import logging

from .models import HistoriaClinica, Diagnostico, Medicamento, Observacion, Cita

audit_logger = logging.getLogger("audit")

# Utilidad para obtener usuario si está disponible
def get_user_from_request(instance):
    try:
        request = getattr(instance, "_request", None)
        if request and hasattr(request, "user"):
            return request.user
    except:
        pass
    return None


# ============================================================
# AUDITORÍA DE ELIMINACIÓN – DIAGNÓSTICOS
# ============================================================
@receiver(post_delete, sender=Diagnostico)
def audit_delete_diagnostico(sender, instance, **kwargs):
    usuario = get_user_from_request(instance)
    audit_logger.info(
        f"[AUDITORÍA] Diagnóstico eliminado | ID {instance.id} | Historia {instance.historia_id} | "
        f"Descripción: {instance.descripcion} | "
        f"Usuario: {usuario if usuario else 'Desconocido'} | Fecha: {timezone.now()}"
    )


# ============================================================
# AUDITORÍA DE ELIMINACIÓN – MEDICAMENTOS
# ============================================================
@receiver(post_delete, sender=Medicamento)
def audit_delete_medicamento(sender, instance, **kwargs):
    usuario = get_user_from_request(instance)
    audit_logger.info(
        f"[AUDITORÍA] Medicamento eliminado | ID {instance.id} | Historia {instance.historia_id} | "
        f"Nombre: {instance.nombre} | "
        f"Usuario: {usuario if usuario else 'Desconocido'} | Fecha: {timezone.now()}"
    )


# ============================================================
# AUDITORÍA DE ELIMINACIÓN – OBSERVACIONES
# ============================================================
@receiver(post_delete, sender=Observacion)
def audit_delete_observacion(sender, instance, **kwargs):
    usuario = get_user_from_request(instance)
    audit_logger.info(
        f"[AUDITORÍA] Observación eliminada | ID {instance.id} | Historia {instance.historia_id} | "
        f"Detalle: {instance.detalle[:120]}... | "
        f"Usuario: {usuario if usuario else 'Desconocido'} | Fecha: {timezone.now()}"
    )


# ============================================================
# AUDITORÍA DE ELIMINACIÓN – CITAS
# ============================================================
@receiver(post_delete, sender=Cita)
def audit_delete_cita(sender, instance, **kwargs):
    usuario = get_user_from_request(instance)
    audit_logger.info(
        f"[AUDITORÍA] Cita eliminada | ID {instance.id} | Historia {instance.historia_id} | "
        f"Motivo: {instance.motivo} | Estado: {instance.estado} | "
        f"Usuario: {usuario if usuario else 'Desconocido'} | Fecha: {timezone.now()}"
    )

# ============================================================
# AUDITORÍA DE ELIMINACIÓN – HISTORIA CLÍNICA
# ============================================================
@receiver(post_delete, sender=HistoriaClinica)
def audit_delete_historia(sender, instance, **kwargs):
    usuario = get_user_from_request(instance)
    audit_logger.info(
        f"[AUDITORÍA] Historia Clínica eliminada | ID {instance.id} | "
        f"Paciente: {instance.paciente.nombre_completo} | "
        f"Usuario: {usuario if usuario else 'Desconocido'} | Fecha: {timezone.now()}"
    )
