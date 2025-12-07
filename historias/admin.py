from django.contrib import admin
from .models import HistoriaClinica

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    # Columnas que se muestran en el listado
    list_display = [
        'numero_historia',
        'paciente',
        'medico_responsable',
        'fecha_ingreso',
        'tipo_historia',
    ]

    # Filtros laterales en el admin
    list_filter = [
        'medico_responsable',
        'fecha_ingreso',
        'tipo_historia',
    ]

    # Búsquedas por campos relacionados
    search_fields = [
        'numero_historia',
        'paciente__nombre_completo',
        'medico_responsable__username',
        'motivo_consulta',
    ]

    # Campos de solo lectura para control de auditoría
    readonly_fields = [
        'created_at',
        'updated_at',
        'fecha_impresion',
    ]

    # Campos a mostrar en el formulario de edición/creación
    fieldsets = (
        ('Datos del Prestador', {
            'fields': (
                'codigo_prestador',
                'nit_prestador',
                'direccion_prestador',
                'telefono_prestador',
                'web_prestador',
                'email_prestador',
            )
        }),
        ('Datos del Paciente', {
            'fields': (
                'paciente',
                'fecha_ingreso',
                'hora_ingreso',
                'fecha_cierre',
                'numero_historia',
                'tipo_historia',
                'usuario_registra',
            )
        }),
        ('Datos de la Historia Clínica', {
            'fields': (
                'medico_responsable',
                'motivo_consulta',
                'puerta_entrada',
                'resumen_clinico',
                'notas_adicionales',
            )
        }),
        ('Control', {
            'fields': (
                'created_at',
                'updated_at',
                'fecha_impresion',
            )
        }),
    )
