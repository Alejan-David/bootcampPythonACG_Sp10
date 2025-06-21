from django.db import models

class MascotaDB(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    dueno = models.ForeignKey('DuenoDB', on_delete=models.CASCADE)
    activo = models.CharField(max_length=1, choices=[('s', 'Sí'), ('n', 'No')])

    def __str__(self):
        return self.nombre

class DuenoDB(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    activo = models.CharField(max_length=1, choices=[('s', 'Sí'), ('n', 'No')], default='s')

    def __str__(self):
        return self.nombre
    
class ConsultaDB(models.Model):
    fecha = models.DateField()
    motivo = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=200)
    mascota = models.ForeignKey('MascotaDB', on_delete=models.CASCADE)
    activo = models.CharField(max_length=1, choices=[('s', 'Sí'), ('n', 'No')])

    def __str__(self):
        return f"{self.fecha} - {self.motivo}"