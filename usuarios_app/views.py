from django.shortcuts import render

# usuarios_app/views.py
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
