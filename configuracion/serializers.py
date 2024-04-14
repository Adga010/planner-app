from rest_framework import serializers
from .models import Proceso, Linea, Cliente, Tipo


class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = ["id", "nombre"]


class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = ["id", "nombre"]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre"]


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = ["id", "nombre"]
