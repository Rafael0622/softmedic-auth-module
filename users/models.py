from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager que usa el correo electrónico como identificador principal."""

    def create_user(self, correo, nombre, rol='RECEPCIONISTA', password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico válido.")

        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, rol=rol, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(correo, nombre, rol='ADMIN', password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado para SoftMedic."""

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('MEDICO', 'Médico'),
        ('RECEPCIONISTA', 'Recepcionista'),
        ('PACIENTE', 'Paciente'),
    ]

    nombre = models.CharField(max_length=150, verbose_name='Nombre completo')
    correo = models.EmailField(unique=True, verbose_name='Correo electrónico')
    rol = models.CharField(max_length=20, choices=ROLES, default='RECEPCIONISTA', verbose_name='Rol')

    # Control Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"

    @property
    def username(self):
        """Propiedad para compatibilidad con templates que usan {{ user.username }}"""
        return self.nombre  # Puedes cambiar a f"{self.first_name} {self.last_name}" si quieres

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre']
