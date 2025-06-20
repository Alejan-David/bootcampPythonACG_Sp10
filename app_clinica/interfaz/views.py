from django.shortcuts import render, redirect
from app_clinica.models import DuenoDB
from app_clinica.interfaz.forms import MascotaForm, DuenoForm, ConsultaForm

def inicio(request):
    return render(request, 'interfaz/inicio.html')

def servicios(request):
    return render(request, 'interfaz/servicios.html')

def menu_mascotas(request):
    mensaje = ''
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento_dueno']
            if DuenoDB.objects.filter(documento=documento).exists():
                form.save()
                mensaje = "Mascota guardada correctamente."
            else:
                mensaje = "⚠️ Documento del dueño no registrado. Por favor ingréselo primero."
    else:
        form = MascotaForm()

    return render(request, 'interfaz/mascotas.html', {'form': form, 'mensaje': mensaje})

def menu_duenos(request): 
    mensaje = ""
    resultados = []
    form = DuenoForm()
    dueno_encontrado = False

    if request.method == 'GET':
        request.session.pop('documento_encontrado', None)

    elif request.method == 'POST':
        accion = request.POST.get("accion")
        documento = request.POST.get("documento")

        if accion == "registrar":
            form = DuenoForm(request.POST)
            if form.is_valid():
                nuevo = form.save(commit=False)
                nuevo.activo = 's'
                nuevo.save()
                mensaje = "Dueño registrado exitosamente."
                form = DuenoForm()

        elif accion == "buscar":
            if documento:
                try:
                    dueno = DuenoDB.objects.get(documento=documento, activo='s')
                    form = DuenoForm(instance=dueno)
                    resultados = [dueno]
                    request.session['documento_encontrado'] = documento
                    mensaje = "Dueño encontrado."
                    dueno_encontrado = True
                except DuenoDB.DoesNotExist:
                    mensaje = "⚠️ Dueño no encontrado."
                    resultados = []
                    request.session.pop('documento_encontrado', None)
            else:
                mensaje = "⚠️ Debes ingresar un número de documento."

        elif accion == "modificar":
            if 'documento_encontrado' in request.session:
                try:
                    dueno = DuenoDB.objects.get(documento=request.session['documento_encontrado'], activo='s')
                    form = DuenoForm(request.POST, instance=dueno)
                    if form.is_valid():
                        form.save()
                        mensaje = "Dueño modificado con éxito."
                        request.session.pop('documento_encontrado')
                        form = DuenoForm()
                except DuenoDB.DoesNotExist:
                    mensaje = "⚠️ No se encontró el dueño para modificar."
            else:
                mensaje = "⚠️ Primero debes buscar un dueño."

        elif accion == "eliminar":
            if 'documento_encontrado' in request.session:
                try:
                    dueno = DuenoDB.objects.get(documento=request.session['documento_encontrado'], activo='s')
                    dueno.activo = 'n'
                    dueno.save()
                    mensaje = "Dueño eliminado lógicamente."
                    request.session.pop('documento_encontrado')
                    form = DuenoForm()
                except DuenoDB.DoesNotExist:
                    mensaje = "⚠️ Dueño no encontrado para eliminar."
            else:
                mensaje = "⚠️ Primero debes buscar el dueño antes de eliminar."

        elif accion == "listar":
            resultados = DuenoDB.objects.filter(activo='s')

    contexto = {
        'form': form,
        'mensaje': mensaje,
        'resultados': resultados,
        'dueno_encontrado': dueno_encontrado or 'documento_encontrado' in request.session
    }
    return render(request, 'duenos/duenos.html', contexto)

def menu_consultas(request):
    mensaje = ""
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "Consulta registrada exitosamente."
        else:
            mensaje = "Por favor verifica los datos ingresados."
    else:
        form = ConsultaForm()

    return render(request, 'consultas/consultas.html', {'form': form, 'mensaje': mensaje})