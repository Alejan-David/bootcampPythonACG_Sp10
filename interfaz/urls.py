from django.urls import path        # Importa la función `path` para definir rutas.
from . import views                 # Importa las vistas definidas en el archivo `views.py`.

urlpatterns = [
    path('', views.inicio, name='inicio'),            # Ruta raíz del sitio (por ejemplo, "/"), llama a la vista `inicio`.
    path('servicios/', views.servicios, name='servicios'),  # Ruta "/servicios/", llama a la vista `servicios`.
    path('dinamico/', views.dinamico, name='dinamico'),     # Ruta "/dinamico/", llama a la vista `dinamico`.
]