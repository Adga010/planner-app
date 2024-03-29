from django.test import TestCase
from usuarios_app.models import Usuario
from usuarios_app.serializers import UsuarioSerializer
from rest_framework.exceptions import ValidationError
import uuid


class UsuarioSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        unique_username = f"user_{uuid.uuid4()}"
        unique_email = f"{uuid.uuid4()}@example.com"

        cls.user_attributes = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "username": unique_username,
            "email": unique_email,
            "rol": "Administrador",
            "cargo": "Gerente",
            "estado": 1,
            "password": "22222222aaaAaQ@a2",
            "confirm_password": "22222222aaaAaQ@a2",
        }

        cls.serializer = UsuarioSerializer(data=cls.user_attributes)
        assert cls.serializer.is_valid(), cls.serializer.errors
        cls.usuario = cls.serializer.save()

    def test_contains_expected_fields(self):
        """Verifica que el serializador contenga los campos esperados."""
        # Inicializa el serializador con una instancia del usuario, no con data
        serializer = UsuarioSerializer(instance=self.usuario)
        data = serializer.data
        expected_fields = {
            "uuid",
            "nombre",
            "apellido",
            "username",
            "email",
            "rol",
            "cargo",
            "estado",
            "fecha_creacion",
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_user_creation(self):
        """Verifica la creación correcta de un usuario."""
        self.assertIsNotNone(
            self.usuario.uuid, "El usuario debe tener un UUID después de ser creado."
        )
        self.assertEqual(
            self.usuario.username,
            self.user_attributes["username"],
            "Los nombres de usuario deben coincidir.",
        )

    def test_email_format_validation(self):
        """Verifica que el serializador rechace correos electrónicos con formato inválido."""
        invalid_email_user = self.user_attributes.copy()
        invalid_email_user["email"] = "invalid_email"
        serializer = UsuarioSerializer(data=invalid_email_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_username_uniqueness(self):
        """Verifica que el serializador rechace nombres de usuario duplicados."""
        duplicate_username_user = self.user_attributes.copy()
        duplicate_username_user["email"] = f"{uuid.uuid4()}@example.com"
        serializer = UsuarioSerializer(data=duplicate_username_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_passwords_match_validation(self):
        """Verifica que las contraseñas que no coinciden sean rechazadas."""
        unmatched_passwords_user = self.user_attributes.copy()
        unmatched_passwords_user.update(
            {
                "username": f"user_{uuid.uuid4()}",  # Asegurarse de que es único para evitar errores de unicidad.
                "email": f"{uuid.uuid4()}@example.com",  # Asegurarse de que es único por la misma razón.
                "confirm_password": "AnotherPassword",
            }
        )
        serializer = UsuarioSerializer(data=unmatched_passwords_user)
        is_valid = serializer.is_valid()

        self.assertFalse(
            is_valid,
            "El serializador debe ser inválido por contraseñas no coincidentes.",
        )
        # Ajustar la aserción para verificar el campo específico donde se esperan los errores
        self.assertIn(
            "confirm_password",
            serializer.errors,
            "Debe haber un error en 'confirm_password' indicando que las contraseñas no coinciden.",
        )

    def test_password_strength_validation(self):
        """Verifica la validación de la fortaleza de la contraseña."""
        weak_password_user = self.user_attributes.copy()
        weak_password_user["password"] = "12345"
        weak_password_user["confirm_password"] = "12345"
        serializer = UsuarioSerializer(data=weak_password_user)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


# Aquí puedes agregar más pruebas según sea necesario
