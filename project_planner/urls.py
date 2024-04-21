# project_planner/urls.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def root_view(request):
    return JsonResponse({"message": "Bienvenido a mi API"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("usuarios_app.urls")),
    path("api/", include("proyectos.urls")),
    path("api/", include("configuracion.urls")),
    path("", root_view),  # Agrega esta línea para la ruta raíz
]
