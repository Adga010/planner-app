# project_planner/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("usuarios_app.urls")),  # Asegúrate de tener esta línea
    path("api/", include("proyectos.urls")),  # Asegúrate de tener esta línea
]
