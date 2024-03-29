from django.contrib import admin
from .models import Planeacion, Estimacion, DisenoCP, Ejecucion


@admin.register(Planeacion)
class PlaneacionAdmin(admin.ModelAdmin):
    list_display = ("proyecto", "tipo_actividad", "fecha")
    list_filter = ("tipo_actividad",)
    search_fields = ("proyecto__nombre",)


admin.site.register(Estimacion)
admin.site.register(DisenoCP)
admin.site.register(Ejecucion)


# jesus alexander andrade.