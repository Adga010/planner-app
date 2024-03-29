# usuarios_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .sesion import LoginView
from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r"usuarios", UsuarioViewSet, basename="usuario")

urlpatterns = [
    path("login/", LoginView.as_view(), name="api-login"),
    path("", include(router.urls)),
]
