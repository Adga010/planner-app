from django.contrib import admin
from .models import Proceso, Linea, Cliente, Tipo

admin.site.register(Proceso)
admin.site.register(Linea)
admin.site.register(Cliente)
admin.site.register(Tipo)
