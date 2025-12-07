from django.apps import AppConfig

class HistoriasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historias'

    def ready(self):
        # Importa signals para registrar permisos y auditoría
        import historias.signals
