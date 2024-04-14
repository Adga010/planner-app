from django.shortcuts import render
from .models import Proceso, Linea, Cliente, Tipo
from .serializers import (
    ProcesoSerializer,
    LineaSerializer,
    ClienteSerializer,
    TipoSerializer,
)


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response


class ListaCombinadaAPIView(APIView):
    def get(self, request, *args, **kwargs):
        procesos = Proceso.objects.all()
        lineas = Linea.objects.all()
        clientes = Cliente.objects.all()
        tipos = Tipo.objects.all()

        response = {
            "procesos": ProcesoSerializer(procesos, many=True).data,
            "lineas": LineaSerializer(lineas, many=True).data,
            "clientes": ClienteSerializer(clientes, many=True).data,
            "tipos": TipoSerializer(tipos, many=True).data,
        }

        return Response(response)
