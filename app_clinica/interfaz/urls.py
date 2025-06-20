from django.urls import path        # Importa la función `path` para definir rutas.
from app_clinica.interfaz import views              # Importa las vistas definidas en el archivo `views.py`.

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('mascotas/', views.menu_mascotas, name='menu_mascotas'),
    path('duenos/', views.menu_duenos, name='menu_duenos'),
    path('consultas/', views.menu_consultas, name='menu_consultas'),
]