from django.db import models
from django.conf import settings
import uuid
from configuracion.models import Proceso, Linea, Tipo, Cliente


class Proyecto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, null=False)
    linea = models.ForeignKey(Linea, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    nombre = models.CharField(max_length=100, unique=True)
    tarea_tw = models.URLField()  # Si es un link URL
    desarrollador = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Quién creó el proyecto

    def __str__(self):
        return self.nombre
