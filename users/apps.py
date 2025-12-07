from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Carga las señales para asignar automáticamente grupos
        según el rol de cada usuario nuevo.
        """
        import users.signals  # 👈 Importa las señales cuando la app está lista
