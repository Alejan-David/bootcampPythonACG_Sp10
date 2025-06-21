from django.shortcuts import render, redirect
from app_clinica.models import DuenoDB,MascotaDB,ConsultaDB
from app_clinica.interfaz.forms import MascotaForm, DuenoForm, ConsultaForm

def inicio(request):
    return render(request, 'interfaz/inicio.html')

def servicios(request):
    return render(request, 'interfaz/servicios.html')

def menu_mascotas(request):
    mensaje = ""
    resultados = []
    form = None
    mascota_encontrada = False
    documento_dueño = ""

    if request.method == 'GET':
        request.session.pop('documento_mascota', None)

    elif request.method == 'POST':
        accion = request.POST.get("accion")
        documento_dueño = request.POST.get("documento_dueno")

        if accion == "buscar":
            if documento_dueño:
                if DuenoDB.objects.filter(documento=documento_dueño, activo='s').exists():
                    try:
                        mascota = MascotaDB.objects.get(dueno__documento=documento_dueño, activo='s')
                        form = MascotaForm(instance=mascota)
                        resultados = [mascota]
                        mensaje = "Mascota encontrada para este dueño."
                        mascota_encontrada = True
                    except MascotaDB.DoesNotExist:
                        form = MascotaForm()
                        mensaje = "Dueño registrado. Puedes ingresar una nueva mascota."
                    request.session['documento_mascota'] = documento_dueño
                else:
                    mensaje = "⚠️ El documento del dueño no está registrado. Por favor regístralo primero."
            else:
                mensaje = "⚠️ Debes ingresar el documento del dueño para buscar."

        elif accion == "registrar":
            form = MascotaForm(request.POST)
            if form.is_valid():
                documento = request.session.get('documento_mascota')
                if DuenoDB.objects.filter(documento=documento, activo='s').exists():
                    dueno = DuenoDB.objects.get(documento=documento, activo='s')
                    nueva = form.save(commit=False)
                    nueva.dueno = dueno
                    nueva.activo = 's'
                    nueva.save()
                    mensaje = "Mascota registrada correctamente."
                    request.session.pop('documento_mascota', None)
                    form = None
                else:
                    mensaje = "⚠️ El documento del dueño no está registrado. No se puede guardar la mascota."

        elif accion == "modificar":
            if 'documento_mascota' in request.session:
                try:
                    mascota = MascotaDB.objects.get(dueno__documento=request.session['documento_mascota'], activo='s')
                    form = MascotaForm(request.POST, instance=mascota)
                    if form.is_valid():
                        form.save()
                        mensaje = "Mascota modificada con éxito."
                        request.session.pop('documento_mascota')
                        form = None
                except MascotaDB.DoesNotExist:
                    mensaje = "⚠️ No se encontró la mascota para modificar."
            else:
                mensaje = "⚠️ Primero debes buscar la mascota."

        elif accion == "eliminar":
            if 'documento_mascota' in request.session:
                try:
                    mascota = MascotaDB.objects.get(dueno__documento=request.session['documento_mascota'], activo='s')
                    mascota.activo = 'n'
                    mascota.save()
                    mensaje = "Mascota eliminada lógicamente."
                    request.session.pop('documento_mascota')
                    form = None
                except MascotaDB.DoesNotExist:
                    mensaje = "⚠️ Mascota no encontrada para eliminar."
            else:
                mensaje = "⚠️ Primero debes buscar la mascota antes de eliminar."

        elif accion == "listar":
            resultados = MascotaDB.objects.filter(activo='s')
            form = None

    contexto = {
        'form': form,
        'mensaje': mensaje,
        'resultados': resultados,
        'mascota_encontrada': mascota_encontrada or 'documento_mascota' in request.session
    }

    return render(request, 'interfaz/mascotas.html', contexto)

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
    resultados = []
    form = None
    consulta_encontrada = False

    if request.method == 'GET':
        request.session.pop('documento_consulta', None)
        request.session.pop('id_consulta_modificar', None)

    elif request.method == 'POST':
        accion = request.POST.get("accion")
        documento_dueno = request.POST.get("documento_dueno")
        consulta_id = request.POST.get("consulta_id")

        if accion == "buscar":
            if documento_dueno:
                try:
                    mascota = MascotaDB.objects.get(dueno__documento=documento_dueno, activo='s')
                    form = ConsultaForm()
                    mensaje = f"Mascota encontrada: {mascota.nombre}."
                    request.session['documento_consulta'] = documento_dueno
                except MascotaDB.DoesNotExist:
                    mensaje = "⚠️ No se encontró mascota para ese documento."
            else:
                mensaje = "⚠️ Debes ingresar el documento."

        elif accion == "registrar":
            form = ConsultaForm(request.POST)
            if form.is_valid():
                documento = request.session.get('documento_consulta')
                try:
                    mascota = MascotaDB.objects.get(dueno__documento=documento, activo='s')
                    nueva = form.save(commit=False)
                    nueva.mascota = mascota
                    nueva.activo = 's'
                    nueva.save()
                    mensaje = "Consulta registrada exitosamente."
                    form = ConsultaForm()
                except MascotaDB.DoesNotExist:
                    mensaje = "⚠️ Mascota no encontrada."
            else:
                mensaje = "⚠️ Datos inválidos."

        elif accion == "listar":
            resultados = ConsultaDB.objects.filter(activo='s').select_related('mascota', 'mascota__dueno')

        elif accion == "cargar_modificar":
            try:
                consulta = ConsultaDB.objects.get(id=consulta_id, activo='s')
                form = ConsultaForm(instance=consulta)
                request.session['id_consulta_modificar'] = consulta.id
                mensaje = f"Consulta cargada para modificar: {consulta.fecha}."
                consulta_encontrada = True
            except ConsultaDB.DoesNotExist:
                mensaje = "⚠️ Consulta no encontrada."

        elif accion == "modificar":
            consulta_id = request.session.get('id_consulta_modificar')
            if consulta_id:
                consulta = ConsultaDB.objects.get(id=consulta_id)
                form = ConsultaForm(request.POST, instance=consulta)
                if form.is_valid():
                    form.save()
                    mensaje = "Consulta modificada exitosamente."
                    form = None
                    request.session.pop('id_consulta_modificar')
                else:
                    mensaje = "⚠️ Datos inválidos para modificar."

        elif accion == "eliminar":
            try:
                consulta = ConsultaDB.objects.get(id=consulta_id)
                consulta.activo = 'n'
                consulta.save()
                mensaje = "Consulta eliminada lógicamente."
            except ConsultaDB.DoesNotExist:
                mensaje = "⚠️ No se encontró la consulta para eliminar."

    # Mostrar todas si no se listó antes
    if not resultados:
        resultados = ConsultaDB.objects.filter(activo='s').select_related('mascota', 'mascota__dueno')

    contexto = {
        'form': form,
        'mensaje': mensaje,
        'resultados': resultados,
        'consulta_encontrada': consulta_encontrada or 'id_consulta_modificar' in request.session
    }
    return render(request, 'consultas/consultas.html', contexto)