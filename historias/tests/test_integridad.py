# =============================================================================
# Proyecto: SOFT-MEDIC
# Archivo: historias/tests.py
# Versión: 1.5
# Fecha: 02/12/2025
# Elaborado por: Prixma Software Projects
# Revisado por: Dirección Técnica de SOFT-MEDIC
# =============================================================================

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from datetime import date

from pacientes.models import Paciente, EPS
from historias.models import HistoriaClinica

User = get_user_model()  # Tu CustomUser


class IntegridadReferencialTest(TestCase):
    """
    Pruebas de integridad referencial entre:
    - Paciente
    - Historia Clínica (HCE)
    """

    def setUp(self):
        # Crear usuario médico responsable usando CustomUser
        self.medico = User.objects.create_user(
            correo='dr.gomez@test.com',
            nombre='Carlos',
            rol='MEDICO',
            password='12345'
        )

        # Crear EPS de prueba
        self.eps = EPS.objects.create(nombre="Salud Total")

        # Crear paciente de prueba
        self.paciente = Paciente.objects.create(
            nombre_completo="Juan Pérez",
            identificacion="123456789",
            fecha_nacimiento=date(1985, 5, 10),
            contacto="555-1234",
            eps=self.eps
        )

        # Crear historia clínica asociada
        self.historia = HistoriaClinica.objects.create(
            paciente=self.paciente,
            medico_responsable=self.medico,
            resumen_clinico="Consulta inicial por dolor abdominal.",
            notas_adicionales="Se recomienda ultrasonido abdominal."
        )

    # -------------------------------------------------------------------------

    def test_historia_asociada_a_paciente(self):
        """Verifica que una historia queda correctamente asociada a un paciente."""
        historia = HistoriaClinica.objects.get(paciente=self.paciente)
        self.assertEqual(historia.paciente.nombre_completo, "Juan Pérez")

    # -------------------------------------------------------------------------

    def test_eliminar_paciente_elimina_historia(self):
        """Al eliminar un paciente, su historia clínica debe eliminarse en cascada."""
        self.paciente.delete()
        historias_restantes = HistoriaClinica.objects.count()
        self.assertEqual(historias_restantes, 0)

    # -------------------------------------------------------------------------

    def test_no_crear_historia_sin_paciente(self):
        """No debe permitirse crear historia clínica sin paciente."""
        with self.assertRaises(IntegrityError):
            HistoriaClinica.objects.create(
                paciente=None,
                medico_responsable=self.medico,
                resumen_clinico="Historia sin paciente"
            )

# =============================================================================
# CONTROL DE CAMBIOS
# ----------------------------------------------------------------------------- 
# Versión | Fecha       | Autor / Responsable          | Descripción de cambios
# 1.0     | 23/11/2025  | Prixma Software Projects     | Creación del archivo y pruebas base
# 1.1     | 02/12/2025  | Prixma Software Projects     | Refactorización de tests para buenas prácticas y consistencia
# 1.2     | 02/12/2025  | Prixma Software Projects     | Adaptación de tests para CustomUser y campos obligatorios
# 1.3     | 02/12/2025  | Prixma Software Projects     | Eliminación de 'username' y compatibilidad total con CustomUser
# 1.4     | 02/12/2025  | Prixma Software Projects     | Eliminación de 'apellido' para compatibilidad con CustomUser
# 1.5     | 02/12/2025  | Prixma Software Projects     | Creación de EPS de prueba y asignación correcta al paciente
# =============================================================================
