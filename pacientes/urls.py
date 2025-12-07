# -------------------------------------------------------------------
# Proyecto: SOFT-MEDIC
# Archivo: softmedic/pacientes/urls.py
# Versión: 1.1
# Fecha: 02/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# -------------------------------------------------------------------
"""
Rutas URL para el módulo de pacientes del sistema SOFT-MEDIC.
Incluye rutas funcionales para el manejo de operaciones CRUD de pacientes
y búsqueda/filtrado.
"""

# -------------------------------------------------------------------
# Importaciones
# -------------------------------------------------------------------
from django.urls import path
from . import views

# -------------------------------------------------------------------
# Configuración del namespace
# -------------------------------------------------------------------
app_name = "pacientes"

# -------------------------------------------------------------------
# Definición de rutas
# -------------------------------------------------------------------
urlpatterns = [
    path("", views.listar_pacientes, name="listar_pacientes"),
    path("registrar/", views.registrar_paciente, name="registrar_paciente"),
    path("editar/<int:pk>/", views.editar_paciente, name="editar_paciente"),
    path("buscar/", views.buscar_pacientes, name="buscar_pacientes"),  # Nueva ruta de búsqueda
]

# -------------------------------------------------------------------
# Control de cambios
# -------------------------------------------------------------------
# | Versión | Fecha       | Autor / Responsable                                   | Descripción de cambios                                         |
# |---------|------------|--------------------------------------------------------|----------------------------------------------------------------|
# | 1.0     | 13/11/2025 | Equipo de Arquitectura y Análisis Técnico Soft-Medic  | Definición base de rutas con estructura estándar de proyecto. |
# | 1.1     | 02/12/2025 | Prixma Software Projects                                | Añadida ruta para búsqueda y filtrado de pacientes           |
