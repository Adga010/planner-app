from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Proyecto, Proceso, Linea, Tipo, Cliente
from django.core.validators import URLValidator

# Mensajes de error comunes para campos de relaciones ForeignKey en el serializador.
COMMON_ERROR_MESSAGES = {
    "required": "Este campo es requerido.",
    "does_not_exist": "El objeto relacionado no existe.",
    "invalid": "ID inválido.",
}


class ProyectoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Proyecto.

    Convierte instancias del modelo Proyecto de/desde formatos JSON.
    Proporciona validación para los campos del modelo y puede incluir lógica de negocio adicional
    para el manejo de proyectos.

    Campos:
    - proceso: Relación ForeignKey con el modelo Proceso.
    - linea: Relación ForeignKey con el modelo Linea.
    - tipo: Relación ForeignKey con el modelo Tipo.
    - cliente: Relación ForeignKey con el modelo Cliente, opcional.
    - tarea_tw: Campo de URL, requiere una URL válida.
    - nombre: Campo de texto que debe ser único.
    - desarrollador: Campo de texto, solo caracteres alfabéticos y espacios permitidos.

    Métodos de validación:
    - validate_nombre: Asegura que el nombre del proyecto sea único.
    - validate_desarrollador: Valida que el desarrollador contenga solo letras y espacios.
    """

    proceso_nombre = serializers.ReadOnlyField(source="proceso.nombre")
    linea_nombre = serializers.ReadOnlyField(source="linea.nombre")
    tipo_nombre = serializers.ReadOnlyField(source="tipo.nombre")
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")

    proceso = serializers.PrimaryKeyRelatedField(
        queryset=Proceso.objects.all(),
        error_messages=COMMON_ERROR_MESSAGES,
    )
    linea = serializers.PrimaryKeyRelatedField(
        queryset=Linea.objects.all(),
        error_messages=COMMON_ERROR_MESSAGES,
    )
    tipo = serializers.PrimaryKeyRelatedField(
        queryset=Tipo.objects.all(),
        error_messages=COMMON_ERROR_MESSAGES,
    )
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        error_messages=COMMON_ERROR_MESSAGES,
    )

    tarea_tw = serializers.URLField(
        error_messages={
            "invalid": "Ingrese una URL válida.",
            "blank": "El Enlace del proyecto no puede estar en blanco.",
        }
    )
    nombre = serializers.CharField(
        error_messages={
            "blank": "El nombre del proyecto no puede estar en blanco.",
            "required": "El nombre del proyecto es obligatorio.",
        }
    )
    desarrollador = serializers.CharField(
        error_messages={
            "blank": "El desarrollador del proyecto no puede estar en blanco.",
            "required": "El desarrollador del proyecto es obligatorio.",
        }
    )

    def validate_nombre(self, value):
        """
        Valida que el nombre del proyecto sea único.

        Parámetros:
        - value: El nombre del proyecto a validar.

        Retorna:
        - El valor validado.

        Excepciones:
        - ValidationError: Si el nombre ya existe.
        """
        value = value.strip()
        if Proyecto.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("El nombre del proyecto ya existe.")
        return value

    def validate_desarrollador(self, value):
        """
        Valida que el desarrollador solo contenga letras y espacios.

        Parámetros:
        - value: El nombre del desarrollador a validar.

        Retorna:
        - El valor validado.

        Excepciones:
        - ValidationError: Si el nombre contiene caracteres no permitidos.
        """
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "El desarrollador solo debe contener letras y espacios."
            )
        return value

    class Meta:
        model = Proyecto
        extra_kwargs = {"creador": {"required": False}}
        fields = [
            "id",
            "proceso",
            "linea",
            "tipo",
            "cliente",
            "nombre",
            "tarea_tw",
            "desarrollador",
            "fecha_creacion",
            "creador",
            "proceso_nombre",
            "linea_nombre",
            "tipo_nombre",
            "cliente_nombre",
        ]
