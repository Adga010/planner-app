from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.dateparse import parse_datetime
import pytz  # Django utiliza la zona horaria definida en settings.py, asegúrate de usar la misma zona horaria aquí.


User = get_user_model()


class UsuarioAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un usuario para pruebas de autenticación
        cls.test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        cls.url = reverse("usuario-list")
        cls.data = {
            "nombre": "Nuevo",
            "apellido": "Usuario",
            "username": "nuevousuario",
            "email": "nuevo@example.com",
            "rol": "Administrador",
            "cargo": "Gerente",
            "estado": 1,
            "password": "22222222aaaAaQ@a2",
            "confirm_password": "22222222aaaAaQ@a2",
        }

    def login(self):
        login_url = reverse("api-login")
        login_data = {"username": "testuser", "password": "testpassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_usuario(self):
        """
        Asegurar que podemos crear un nuevo usuario a través de la API.
        """
        self.login()  # Autenticarse antes de la solicitud
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.data["email"]).exists())

    def test_create_usuario_empty_fields(self):
        """
        Asegurar que no podemos crear un nuevo usuario sin username o email a través de la API.
        """
        self.login()  # Autenticarse antes de la solicitud
        self.data.update({"username": "", "email": ""})
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_create_usuario_unique_fields(self):
        """
        Asegurar que no podemos crear un nuevo usuario con username o email que ya existen a través de la API.
        """
        self.login()  # Autenticarse antes de la solicitud
        self.data.update(
            {"username": self.test_user.username, "email": self.test_user.email}
        )
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_create_usuario_date_validation(self):
        """
        Asegurar que la fecha de creación del usuario es la correcta.
        """
        self.login()  # Autenticarse antes de la solicitud.
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Convertir la fecha de creación de string a datetime.
        fecha_creacion_str = response.data.get("fecha_creacion")
        fecha_creacion = parse_datetime(fecha_creacion_str)

        # Obtener la fecha/hora actual.
        now = datetime.now(
            pytz.timezone("UTC")
        )  # Asegúrate de usar la misma zona horaria que tu proyecto Django.

        # Comprobar que la fecha de creación es reciente, por ejemplo, menos de un minuto de antigüedad.
        self.assertTrue(
            (now - fecha_creacion).seconds < 60, "La fecha de creación no es reciente."
        )
