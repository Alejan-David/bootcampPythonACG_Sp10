# Generated by Django 5.2.3 on 2025-06-21 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DuenoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.CharField(max_length=200)),
                ('activo', models.CharField(choices=[('s', 'Sí'), ('n', 'No')], default='s', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='MascotaDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('especie', models.CharField(max_length=100)),
                ('raza', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('activo', models.CharField(choices=[('s', 'Sí'), ('n', 'No')], max_length=1)),
                ('dueno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_clinica.duenodb')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultaDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('motivo', models.CharField(max_length=200)),
                ('diagnostico', models.CharField(max_length=200)),
                ('activo', models.CharField(choices=[('s', 'Sí'), ('n', 'No')], max_length=1)),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_clinica.mascotadb')),
            ],
        ),
    ]
