from django.db import models
from proyectos.models import Proyecto
from django.conf import settings

## Planeaciones

class Planeacion(models.Model):
    TIPO_ACTIVIDAD_CHOICES = [
        ("estimacion", "Estimación"),
        ("diseno_cp", "Diseño CP"),
        ("ejecucion", "Ejecución"),
        ("finalizado", "Finalizado"),
    ]

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="planeaciones"
    )
    tipo_actividad = models.CharField(max_length=20, choices=TIPO_ACTIVIDAD_CHOICES)
    fecha = models.DateField()

    class Meta:
        unique_together = (("proyecto", "tipo_actividad"),)

    def __str__(self):
        return f"{self.get_tipo_actividad_display()} para {self.proyecto.nombre}"


## Trazabilidad

ITERACION_CHOICES = [
    ("iteracion_1", "Iteración 1"),
    ("iteracion_2", "Iteración 2"),
    ("iteracion_3", "Iteración 3"),
]


class Estimacion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_registro_real = models.DateField()
    horas_est_dcp = models.DecimalField(max_digits=5, decimal_places=2)
    horas_est_eje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_entrega_hu = models.DateField()
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Estimación para {self.proyecto.nombre}"


class DisenoCP(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_registro_real = models.DateField()
    horas_real_dcp = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Diseño CP para {self.proyecto.nombre}"


class Ejecucion(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_registro_real = models.DateField()
    iteracion = models.CharField(max_length=50, choices=ITERACION_CHOICES)
    horas_real_eje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Ejecución para {self.proyecto.nombre} - {self.get_iteracion_display()}"
