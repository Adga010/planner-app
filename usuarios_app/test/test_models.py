from django.test import TestCase
from usuarios_app.models import Usuario
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate


class UsuarioModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configura un objeto de usuario para usar en todas las pruebas de esta clase.
        cls.usuario = Usuario.objects.create_user(
            email="test@test.com",
            username="testuser",
            password="securepassword",
            nombre="Test",
            apellido="User",
        )

    def test_email_uniqueness(self):
        """
        Prueba que no se pueden crear dos usuarios con el mismo email.
        Se espera una excepción de IntegrityError debido a la restricción de unicidad.
        """
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                email="test@test.com", username="newtestuser", password="newpassword"
            )

    def test_username_uniqueness(self):
        """
        Prueba que no se pueden crear dos usuarios con el mismo username.
        Se espera una excepción de IntegrityError debido a la restricción de unicidad.
        """
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                email="test1@test.com", username="testuser", password="newpassword"
            )

    def test_username_email_uniqueness(self):
        """
        Prueba que no se pueden crear dos usuarios con el mismo email y username.
        Se espera una excepción de IntegrityError debido a las restricciones de unicidad.
        """
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                email="test@test.com", username="testuser", password="securepassword"
            )

    def test_get_full_name(self):
        """
        Prueba que el método get_full_name del modelo de usuario retorna el nombre completo.
        """
        self.assertEqual(self.usuario.get_full_name(), "Test User")

    def test_get_short_name(self):
        """
        Prueba que el método get_short_name del modelo de usuario retorna el primer nombre.
        """
        self.assertEqual(self.usuario.get_short_name(), "Test")

    def test_password_is_hashed_on_creation(self):
        """
        Prueba que la contraseña se hashea al crear el usuario y que se puede verificar con check_password.
        """
        self.assertTrue(self.usuario.password != "securepassword")
        self.assertTrue(self.usuario.check_password("securepassword"))

    def test_user_authentication(self):
        """
        Prueba que un usuario puede autenticarse con las credenciales correctas.
        """
        usuario = authenticate(username="testuser", password="securepassword")
        self.assertIsNotNone(usuario)

    def test_required_fields(self):
        """
        Prueba que se lanzará un error si se intenta crear un usuario sin todos los campos requeridos.
        """
        with self.assertRaises(TypeError):
            Usuario.objects.create_user(email="newuser@test.com")

    def test_default_estado(self):
        """
        Prueba que el campo 'estado' del modelo de usuario tiene el valor por defecto esperado.
        """
        usuario = Usuario.objects.get(email="test@test.com")
        self.assertTrue(usuario.estado)

    def test_change_estado(self):
        """
        Prueba que el campo 'estado' del modelo de usuario puede ser cambiado y guardado correctamente.
        """
        usuario = Usuario.objects.get(email="test@test.com")
        usuario.estado = False
        usuario.save()
        usuario.refresh_from_db()
        self.assertFalse(usuario.estado)

    def test_uuid_is_assigned(self):
        """
        Prueba que se asigna un UUID al crear un nuevo usuario.
        """
        usuario = Usuario.objects.get(email="test@test.com")
        self.assertIsNotNone(usuario.uuid)

    def test_fecha_creacion_is_assigned(self):
        """
        Prueba que se asigna automáticamente la fecha de creación al crear un nuevo usuario.
        """
        usuario = Usuario.objects.get(email="test@test.com")
        self.assertIsNotNone(usuario.fecha_creacion)
