from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Crea y devuelve un usuario con un email, nombre de usuario y contraseña.
        """
        if not email:
            raise ValueError(_("El email es obligatorio"))
        if not username:
            raise ValueError(_("El nombre de usuario es obligatorio"))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Asegura que la contraseña se maneje correctamente
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Crea y devuelve un superusuario con un email, nombre de usuario y contraseña.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser debe tener is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que soporta usar email en lugar de nombre de usuario.
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    rol = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",
        blank=True,
        help_text=_("The groups this user belongs to."),
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_user_permissions",
        blank=True,
        help_text=_("Specific permissions for this user."),
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Retorna el nombre completo del usuario.
        """
        return f"{self.nombre} {self.apellido}"

    def get_short_name(self):
        """
        Retorna el nombre corto del usuario.
        """
        return self.nombre
