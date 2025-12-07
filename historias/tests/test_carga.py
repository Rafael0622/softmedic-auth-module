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
from django.utils import timezone
from datetime import date
import time

from pacientes.models import Paciente, EPS
from historias.models import HistoriaClinica

User = get_user_model()  # CustomUser


class IntegridadReferencialTest(TestCase):
    """
    Pruebas de integridad referencial entre:
    - Paciente
    - Historia Clínica (HCE)
    """

    @classmethod
    def setUpTestData(cls):
        cls.medico = User.objects.create_user(
            correo='dr.gomez@test.com',
            nombre='Carlos',
            rol='MEDICO',
            password='12345'
        )
        cls.eps = EPS.objects.create(nombre="EPS Test")

    def setUp(self):
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
        self.assertEqual(HistoriaClinica.objects.count(), 0)

    # -------------------------------------------------------------------------
    def test_no_crear_historia_sin_paciente(self):
        """No debe permitirse crear historia clínica sin paciente."""
        with self.assertRaises(IntegrityError):
            HistoriaClinica.objects.create(
                paciente=None,
                medico_responsable=self.medico,
                resumen_clinico="Historia sin paciente"
            )


class PruebasCargaHCE(TestCase):
    """
    Pruebas de carga masiva y validación de integridad para Historias Clínicas Electrónicas (HCE).
    """

    @classmethod
    def setUpTestData(cls):
        cls.medico = User.objects.create_user(
            correo="medico_pruebas@test.com",
            nombre="Medico Pruebas",
            rol="MEDICO",
            password="123456"
        )
        cls.eps = EPS.objects.create(nombre="EPS Test")

    def crear_historia(self, index):
        paciente = Paciente.objects.create(
            nombre_completo=f"Paciente {index}",
            identificacion=f"1000{index}",
            fecha_nacimiento="1990-01-01",
            contacto="3001234567",
            eps=self.eps
        )

        HistoriaClinica.objects.create(
            paciente=paciente,
            medico_responsable=self.medico,
            motivo_consulta="Prueba de carga",
            resumen_clinico="Lorem ipsum...",
            fecha_ingreso=timezone.now().date()
        )

    # -------------------------------------------------------------------------
    def test_carga_masiva_secuencial(self):
        total = 1000
        inicio = time.time()
        for i in range(total):
            self.crear_historia(i)
        fin = time.time()
        duracion = fin - inicio
        print(f"\n⏱ Tiempo inserción secuencial ({total} HCE): {duracion:.2f} segundos")
        self.assertEqual(HistoriaClinica.objects.count(), total)

    # -------------------------------------------------------------------------
    def test_carga_masiva_bulk_create(self):
        total = 1000
        inicio = time.time()

        pacientes = []
        historias = []

        for i in range(total):
            pacientes.append(Paciente(
                nombre_completo=f"Paciente {i}",
                identificacion=f"1000{i}",
                fecha_nacimiento="1990-01-01",
                contacto="3001234567",
                eps=self.eps
            ))

        Paciente.objects.bulk_create(pacientes)
        pacientes_creados = list(Paciente.objects.all()[:total])

        for paciente in pacientes_creados:
            historias.append(HistoriaClinica(
                paciente=paciente,
                medico_responsable=self.medico,
                motivo_consulta="Prueba de carga",
                resumen_clinico="Lorem ipsum...",
                fecha_ingreso=timezone.now().date()
            ))

        HistoriaClinica.objects.bulk_create(historias)
        fin = time.time()
        duracion = fin - inicio

        print(f"\n⚡ Tiempo inserción masiva ({total} HCE) usando bulk_create: {duracion:.2f} segundos")
        self.assertEqual(HistoriaClinica.objects.count(), total)

    # -------------------------------------------------------------------------
    def test_integridad_post_carga(self):
        self.crear_historia(1)
        self.crear_historia(2)
        self.crear_historia(3)

        self.assertEqual(HistoriaClinica.objects.count(), 3)
        for historia in HistoriaClinica.objects.all():
            self.assertIsNotNone(historia.paciente)
            self.assertIsNotNone(historia.medico_responsable)
            self.assertTrue(historia.fecha_ingreso)


# =============================================================================
# CONTROL DE CAMBIOS
# -----------------------------------------------------------------------------
# Versión | Fecha       | Autor / Responsable          | Descripción de cambios
# 1.0     | 23/11/2025  | Prixma Software Projects     | Creación inicial y pruebas básicas
# 1.1     | 02/12/2025  | Prixma Software Projects     | Adaptación para CustomUser y EPS
# 1.2     | 02/12/2025  | Prixma Software Projects     | Optimización de tests de carga con bulk_create; tests estables y confiables
# 1.5     | 02/12/2025  | Prixma Software Projects     | Consolidación completa de tests de historias, secuencial y masiva
# =============================================================================
