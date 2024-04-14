from rest_framework import viewsets
from .models import Proyecto
from .serializers import ProyectoSerializer
from rest_framework.permissions import IsAuthenticated


class ProyectoViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet para ver y editar los proyectos.

    Este ViewSet utiliza autenticación y requiere que el usuario esté autenticado para acceder a cualquier
    funcionalidad relacionada con los proyectos. Proporciona acciones estándar para listar, crear, actualizar,
    y eliminar proyectos.

    Todos los proyectos creados a través de esta vista automáticamente asignan al usuario autenticado como el creador
    del proyecto.

    Hereda de:
    - ModelViewSet: Proporciona la implementación por defecto para las operaciones CRUD.

    Atributos:
    - permission_classes: Lista de clases de permisos aplicadas a la vista.
    - queryset: El queryset que se utiliza para recuperar los objetos Proyecto.
    - serializer_class: El serializador que se utiliza para la entrada y salida de datos.
    """

    permission_classes = [IsAuthenticated]
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def perform_create(self, serializer):
        """
        Guarda la instancia del proyecto, asegurando que el 'creador' se establece en el usuario autenticado actual.

        Parámetros:
        - serializer: El serializador que contiene los datos validados del proyecto.
        """
        serializer.save(creador=self.request.user)
