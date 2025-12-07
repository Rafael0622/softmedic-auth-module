from django.db import models
from django.conf import settings
from django.utils import timezone


class AuditoriaEliminacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="auditorias_eliminacion"
    )

    modelo_afectado = models.CharField(max_length=100)
    objeto_id = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.modelo_afectado} eliminado (ID {self.objeto_id})"
