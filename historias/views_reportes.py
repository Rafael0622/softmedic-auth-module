# =============================================================
# Proyecto: SOFT-MEDIC
# Archivo: historias/views_reportes.py
# Versión: 1.0
# Fecha: 07/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica SOFT-MEDIC
#
# Descripción:
# Exporta un reporte CSV de pacientes atendidos usando los campos
# reales del modelo HistoriaClinica. Corregido: 'fecha_creacion'
# no existe — ahora se usa 'created_at'.
# =============================================================

from django.http import HttpResponse
from .models import HistoriaClinica
import csv
from datetime import datetime


def reporte_pacientes_atendidos_csv(request):
    """
    Genera un archivo CSV con el listado de pacientes atendidos.
    """

    # Nombre del archivo dinámico
    fecha_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"reporte_pacientes_atendidos_{fecha_str}.csv"

    # Respuesta HTTP tipo archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Encabezado del CSV
    writer.writerow([
        "ID Historia",
        "Paciente",
        "Documento",
        "Sexo",
        "Médico Responsable",
        "Fecha Atención",
        "Motivo Consulta",
        "Diagnósticos"
    ])

    # Consulta optimizada
    historias = HistoriaClinica.objects.select_related(
        "paciente",
        "medico_responsable"
    ).all()

    # Filas del archivo
    for h in historias:

        # Diagnósticos desde JSONField → lista de descripciones
        diag_list = []
        if isinstance(h.diagnosticos, list):
            for d in h.diagnosticos:
                diag_list.append(d.get("descripcion", ""))
        diagnosticos_text = ", ".join(diag_list)

        writer.writerow([
            h.id,
            h.paciente.nombre_completo if hasattr(h.paciente, "nombre_completo") else str(h.paciente),
            getattr(h.paciente, "documento", ""),
            getattr(h.paciente, "sexo", ""),
            h.medico_responsable.nombre if hasattr(h.medico_responsable, "nombre") else h.medico_responsable.get_full_name(),
            h.created_at.strftime("%Y-%m-%d %H:%M"),
            h.motivo_consulta or "",
            diagnosticos_text
        ])

    return response


# =============================================================
# CONTROL DE CAMBIOS
# -------------------------------------------------------------
# Versión | Fecha       | Responsable                  | Descripción
# 1.0     | 07/12/2025  | Prixma Software Projects      | Versión inicial del reporte CSV
# =============================================================
