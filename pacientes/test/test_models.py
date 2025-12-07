from django.test import TestCase
from pacientes.models import Paciente
from datetime import date

class PacienteModelTest(TestCase):

    def setUp(self):
        # Inserción de datos de prueba
        self.p1 = Paciente.objects.create(
            nombre_completo="Juan Pérez",
            identificacion="123456789",
            fecha_nacimiento=date(1985, 5, 10),
            contacto="555-1234",
            eps="Salud Total"
        )
        self.p2 = Paciente.objects.create(
            nombre_completo="María López",
            identificacion="987654321",
            fecha_nacimiento=date(1990, 8, 22),
            contacto="555-5678",
            eps="Coomeva"
        )

    def test_creacion_paciente(self):
        """Prueba tuya: validación básica de creación."""
        self.assertEqual(str(self.p1), "Juan Pérez (123456789)")
        self.assertIsNotNone(self.p1.created_at)

    def test_consulta_paciente_por_identificacion(self):
        paciente = Paciente.objects.get(identificacion="123456789")
        self.assertEqual(paciente.nombre_completo, "Juan Pérez")
        self.assertEqual(paciente.eps, "Salud Total")

    def test_lista_total_pacientes(self):
        pacientes = Paciente.objects.all()
        self.assertEqual(pacientes.count(), 2)
