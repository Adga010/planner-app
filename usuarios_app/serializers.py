from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re

# Obtener el modelo de usuario personalizado
User = get_user_model()


def get_default_error_messages():
    return {
        "blank": _("Este campo no puede estar vacío."),
        "max_length": _("Este campo no puede superar los 50 caracteres."),
    }


def validate_password_strength(value):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad.
    """
    if len(value) < 8 or len(value) > 20:
        raise serializers.ValidationError(
            _("La contraseña debe tener entre 8 y 20 caracteres.")
        )
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError(
            _("La contraseña debe contener al menos un número.")
        )
    if not any(char.isalpha() for char in value):
        raise serializers.ValidationError(
            _("La contraseña debe contener al menos una letra.")
        )
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError(
            _("La contraseña debe contener al menos una letra mayúscula.")
        )
    if not any(char.islower() for char in value):
        raise serializers.ValidationError(
            _("La contraseña debe contener al menos una letra minúscula.")
        )
    if not re.findall("[@#$%^&+=]", value):
        raise serializers.ValidationError(
            _(
                "La contraseña debe contener al menos un carácter especial (ej. @, #, $, etc.)."
            )
        )
    return value


class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        max_length=50, error_messages=get_default_error_messages()
    )
    apellido = serializers.CharField(
        max_length=50, error_messages=get_default_error_messages()
    )
    username = serializers.CharField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_("Este nombre de usuario ya está en uso."),
            )
        ],
        error_messages=get_default_error_messages(),
    )
    email = serializers.EmailField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_("Este correo electrónico ya está en uso."),
            )
        ],
        error_messages={
            "blank": _("Este campo no puede estar vacío."),
            "invalid": _("El formato de correo electrónico no es válido."),
            "max_length": _("Este campo no puede superar los 50 caracteres."),
        },
    )
    rol = serializers.CharField(error_messages=get_default_error_messages())
    cargo = serializers.CharField(error_messages=get_default_error_messages())
    estado = serializers.CharField(error_messages=get_default_error_messages())
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password_strength],
        error_messages={"blank": _("Este campo no puede estar vacío.")},
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True, error_messages={"blank": _("Este campo no puede estar vacío.")}
    )

    class Meta:
        model = User
        fields = [
            "uuid",
            "nombre",
            "apellido",
            "username",
            "email",
            "rol",
            "cargo",
            "estado",
            "fecha_creacion",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate(self, data):
        # Validación de la confirmación de contraseña
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": _("La confirmación de contraseña no coincide.")}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        return user
