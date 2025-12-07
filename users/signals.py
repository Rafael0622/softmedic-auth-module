from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def asignar_grupo_por_rol(sender, instance, created, **kwargs):
    """
    Asigna automáticamente un grupo al usuario según su rol
    cuando se crea un nuevo usuario.
    """
    if created:
        if instance.rol == 'ADMIN':
            grupo, _ = Group.objects.get_or_create(name='Administradores')
        elif instance.rol == 'MEDICO':
            grupo, _ = Group.objects.get_or_create(name='Medicos')
        elif instance.rol == 'RECEPCIONISTA':
            grupo, _ = Group.objects.get_or_create(name='Recepcionistas')
        else:
            grupo = None

        if grupo:
            instance.groups.add(grupo)
