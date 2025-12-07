from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username='admin', password='admin123', rol='ADMIN', nombre='Administrador General'
        )
        self.medico_user = CustomUser.objects.create_user(
            username='medico', password='medico123', rol='MEDICO', nombre='Dr. Juan Pérez'
        )
        self.recepcionista_user = CustomUser.objects.create_user(
            username='recepcionista', password='recep123', rol='RECEPCIONISTA', nombre='María López'
        )

    def test_login_correcto(self):
        """Verifica que un usuario pueda iniciar sesión correctamente"""
        response = self.client.post(reverse('users:login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)  # Redirección exitosa
        self.assertRedirects(response, reverse('users:admin_dashboard'))

    def test_login_incorrecto(self):
        """Verifica que el sistema muestre error con credenciales inválidas"""
        response = self.client.post(reverse('users:login'), {
            'username': 'admin',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos")

    def test_logout(self):
        """Verifica que un usuario autenticado pueda cerrar sesión correctamente"""
        self.client.login(username='medico', password='medico123')
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('users:login'))

    def test_redireccion_por_rol(self):
        """Valida que cada usuario autenticado sea redirigido a su panel correspondiente"""
        users = [
            ('admin', 'admin123', reverse('users:admin_dashboard')),
            ('medico', 'medico123', reverse('users:medico_dashboard')),
            ('recepcionista', 'recep123', reverse('users:recepcionista_dashboard')),
        ]
        for username, password, redirect_url in users:
            response = self.client.post(reverse('users:login'), {
                'username': username, 'password': password
            })
            self.assertRedirects(response, redirect_url)

    def test_acceso_no_autenticado(self):
        """Confirma que un usuario no autenticado sea redirigido al login"""
        response = self.client.get(reverse('users:admin_dashboard'))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('users:admin_dashboard')}")
