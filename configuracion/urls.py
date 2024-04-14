from django.urls import path
from .views import ListaCombinadaAPIView

urlpatterns = [
    path("lista-combinada/", ListaCombinadaAPIView.as_view(), name="lista-combinada"),
]
