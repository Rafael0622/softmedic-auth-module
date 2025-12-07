from django.urls import path
from .views import (
    HistoriaClinicaCreateView,
    HistoriaClinicaUpdateView,
    HistoriaClinicaListView,
    HistoriaClinicaDetailView,
    HistoriaClinicaDeleteView
)
from .views_reportes import reporte_pacientes_atendidos_csv

app_name = 'historias'

urlpatterns = [
    path('', HistoriaClinicaListView.as_view(), name='listar_historias'),
    path('crear/', HistoriaClinicaCreateView.as_view(), name='crear_historia'),
    path('editar/<int:pk>/', HistoriaClinicaUpdateView.as_view(), name='editar_historia'),
    path('<int:pk>/', HistoriaClinicaDetailView.as_view(), name='ver_historia'),
    path('eliminar/<int:pk>/', HistoriaClinicaDeleteView.as_view(), name='eliminar_historia'),

    # ======================================================
    # 📌 REPORTE CSV — Pacientes atendidos
    # ======================================================
    path(
        'reportes/pacientes-atendidos/',
        reporte_pacientes_atendidos_csv,
        name='reporte_pacientes_atendidos'
    ),
]
