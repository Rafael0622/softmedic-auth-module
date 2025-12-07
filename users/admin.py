from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Configuración personalizada del panel de administración
    para gestionar usuarios del sistema SoftMedic.
    """

    # ----------------------------------------------------------------
    # CAMPOS QUE SE MUESTRAN EN LA LISTA DEL ADMIN
    # ----------------------------------------------------------------
    list_display = ('correo', 'nombre', 'rol', 'mostrar_grupos', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('correo', 'nombre')
    ordering = ('nombre',)

    # ----------------------------------------------------------------
    # CAMPOS VISIBLES AL EDITAR UN USUARIO
    # ----------------------------------------------------------------
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información personal', {'fields': ('nombre', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # ----------------------------------------------------------------
    # CAMPOS AL CREAR UN NUEVO USUARIO DESDE EL ADMIN
    # ----------------------------------------------------------------
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'rol', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    # ----------------------------------------------------------------
    # CAMPOS DE SOLO LECTURA
    # ----------------------------------------------------------------
    readonly_fields = ('date_joined', 'last_login')

    # ----------------------------------------------------------------
    # MOSTRAR GRUPOS ASIGNADOS EN LA LISTA
    # ----------------------------------------------------------------
    def mostrar_grupos(self, obj):
        """Muestra los grupos a los que pertenece cada usuario."""
        return ", ".join([g.name for g in obj.groups.all()]) or "—"
    mostrar_grupos.short_description = "Grupos"

    # ----------------------------------------------------------------
    # CONFIGURACIÓN GENERAL
    # ----------------------------------------------------------------
    def get_readonly_fields(self, request, obj=None):
        """
        Hace que ciertos campos sean de solo lectura una vez creado el usuario.
        """
        if obj:  # Si el usuario ya existe
            return self.readonly_fields + ('correo',)
        return self.readonly_fields


# Nota: gracias al decorador @admin.register(CustomUser),
# no hace falta llamar a admin.site.register().
