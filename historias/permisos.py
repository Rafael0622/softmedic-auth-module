# =====================================================================
# Proyecto: SOFT-MEDIC
# Archivo: historias/permisos.py
# Versión: 1.0
# Fecha: 05/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# =====================================================================

from django.http import HttpResponseForbidden


def puede_ver_historia(user, historia):
    if user.rol == "MEDICO" and historia.medico_responsable == user:
        return True
    if user.rol in ["ADMIN", "RECEPCIONISTA"]:
        return True
    return False


def puede_editar_historia(user, historia):
    return user.rol == "MEDICO" and historia.medico_responsable == user


def puede_eliminar_historia(user):
    return user.rol == "ADMIN"
