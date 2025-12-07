from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'identificacion', 'fecha_nacimiento', 'contacto', 'eps')
    search_fields = ('nombre_completo', 'identificacion')
    list_filter = ('eps',)
    ordering = ('nombre_completo',)
