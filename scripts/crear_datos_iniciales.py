# Archivo: scripts/crear_datos_iniciales.py
import os
import django
from django.utils import timezone

# Configurar Django si se ejecuta fuera del manage.py shell
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "softmedic.settings")
django.setup()

from django.contrib.auth import get_user_model
from pacientes.models import Paciente
from historias.models import HistoriaClinica

User = get_user_model()

# ------------------------
# 1. Crear superusuario
# ------------------------
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@softmedic.com',
        password='Admin1234'
    )
    print("Superusuario 'admin' creado.")
else:
    print("Superusuario 'admin' ya existe.")

# ------------------------
# 2. Crear médico
# ------------------------
if not User.objects.filter(username='medico1').exists():
    medico = User.objects.create_user(
        username='medico1',
        email='medico1@softmedic.com',
        password='Medico1234',
        rol='MEDICO'  # Asegúrate de que tu modelo User tenga el campo 'rol'
    )
    print("Usuario médico 'medico1' creado.")
else:
    medico = User.objects.get(username='medico1')
    print("Usuario médico 'medico1' ya existe.")

# ------------------------
# 3. Crear recepcionista
# ------------------------
if not User.objects.filter(username='recepcionista1').exists():
    recepcionista = User.objects.create_user(
        username='recepcionista1',
        email='recepcionista1@softmedic.com',
        password='Recep1234',
        rol='RECEPCIONISTA'  # Campo rol en User
    )
    print("Usuario recepcionista 'recepcionista1' creado.")
else:
    recepcionista = User.objects.get(username='recepcionista1')
    print("Usuario recepcionista 'recepcionista1' ya existe.")

# ------------------------
# 4. Crear pacientes de prueba
# ------------------------
pacientes_data = [
    {"nombre_completo": "Juan Perez", "identificacion": "12345678"},
    {"nombre_completo": "Maria Gomez", "identificacion": "87654321"},
    {"nombre_completo": "Luis Ramirez", "identificacion": "11223344"},
]

for p_data in pacientes_data:
    paciente, created = Paciente.objects.get_or_create(
        identificacion=p_data["identificacion"],
        defaults={"nombre_completo": p_data["nombre_completo"]}
    )
    if created:
        print(f"Paciente '{paciente.nombre_completo}' creado.")
    else:
        print(f"Paciente '{paciente.nombre_completo}' ya existe.")

# ------------------------
# 5. Crear Historia Clínica de prueba
# ------------------------
paciente = Paciente.objects.first()
if paciente and not HistoriaClinica.objects.filter(paciente=paciente, medico_responsable=medico).exists():
    historia = HistoriaClinica.objects.create(
        paciente=paciente,
        medico_responsable=medico,
        motivo_consulta="Consulta general de prueba",
        puerta_entrada="Consultorio externo",
        resumen_clinico="Resumen clínico de prueba",
        numero_historia="HC-001",
        fecha_ingreso=timezone.now(),
        hora_ingreso=timezone.now().time(),
    )
    print(f"Historia Clínica de prueba creada para {paciente.nombre_completo} y médico {medico.username}.")
else:
    print("Historia Clínica de prueba ya existe.")
