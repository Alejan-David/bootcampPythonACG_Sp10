from django.shortcuts import render

def inicio(request):
    return render(request, 'app_clinica/inicio.html')

def servicios(request):
    return render(request, 'app_clinica/servicios.html')

def dinamico(request):
    return render(request, 'app_clinica/dinamico.html')