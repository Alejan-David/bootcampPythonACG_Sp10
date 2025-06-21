from django import forms
from  app_clinica.models import MascotaDB,DuenoDB,ConsultaDB

class MascotaForm(forms.ModelForm):
    class Meta:
        model = MascotaDB
        fields = ['nombre', 'especie', 'raza', 'edad'] 

class DuenoForm(forms.ModelForm):
    class Meta:
        model = DuenoDB
        fields = ['documento', 'nombre', 'telefono', 'direccion'] 


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = ConsultaDB
        exclude = ['mascota', 'activo']  
        