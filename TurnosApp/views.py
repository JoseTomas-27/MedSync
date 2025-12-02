from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
import uuid
from datetime import datetime
from .models import Usuarios
from .permissions import IsAdminUserSession
from django.contrib.auth import authenticate, login, get_user_model
from TurnosApp.models import Administrador
from .forms import UsuarioForm
from django.contrib.auth.decorators import login_required
from .models import Horarios, Enfermeros, Tens
from django.contrib.auth.hashers import make_password, check_password  # ✅ Import para hash
from django.contrib.auth.hashers import make_password  # 👈 Agrega esta importación
import requests


def registro_view(request):
    # Solo permite el acceso si el usuario logueado tiene el rol 'Administrador'
    if request.session.get('usuario_rol') != 'Administrador':
        messages.error(request, 'Solo el administrador puede acceder al registro de usuarios.')
        return redirect('dashboard')

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        # Validaciones
        if Usuarios.objects.filter(rut=rut).exists():
            messages.error(request, 'El RUT ya está registrado.')
        elif Usuarios.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
        else:
            # ✅ Guardar la contraseña hasheada
            Usuarios.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                pass_field=make_password(password),  # <-- Aquí está la corrección
                rol=rol
            )
            messages.success(request, 'Usuario registrado con éxito. Ahora puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'TurnosApp/registro.html')


PACIENTES_DATA = [
    {
        'id': 1,
        'nombre': 'Juan Pérez',
        'rut': '12.345.678-9',
        'sala': 'Sala 101',
        'diagnostico': 'Neumonía',
        'medicamentos': ['Losartán', 'Aspirina'],
        'observaciones': 'Paciente estable, monitorear presión arterial.',
        'pais': 'Chile',
        'fiebre': True,
        'contagio': True
    },
    {
        'id': 2,
        'nombre': 'María González',
        'rut': '9.876.543-2',
        'sala': 'Sala 101',
        'diagnostico': 'Fractura de tobillo',
        'medicamentos': ['Paracetamol', 'Ibuprofeno'],
        'observaciones': 'Requiere asistencia para movilizarse.',
        'pais': 'Argentina',
        'fiebre': False,
        'contagio': False
    },
    {
        'id': 3,
        'nombre': 'Pedro Pascal',
        'rut': '5.555.555-5',
        'sala': 'Sala 102',
        'diagnostico': 'Apendicitis',
        'medicamentos': ['Antibióticos'],
        'observaciones': 'En aislamiento.',
        'pais': 'United States',
        'fiebre': False,
        'contagio': False
    },
    {
        'id': 4,
        'nombre': 'Javiera Flores',
        'rut': '20.111.222-3',
        'sala': 'Sala 103',
        'diagnostico': 'Bronquitis',
        'medicamentos': ['Sumatriptán'],
        'observaciones': 'Control con neumólogo.',
        'pais': 'Brazil',
        'fiebre': True,
        'contagio': False
    },
]


REPORTES_DATA = [
    {'id': 'reporte-1-sofia', 'autor': 'Sofía Rodríguez', 'fecha': '12 de Octubre de 2025', 'contenido': 'Se reporta una falla en el monitor de signos vitales de la sala 102. Se ha notificado a mantenimiento.'},
    {'id': 'reporte-2-carlos', 'autor': 'Carlos Pérez', 'fecha': '11 de Octubre de 2025', 'contenido': 'El paciente Juan Pérez de la sala 101 presentó una leve reacción alérgica al medicamento administrado por la mañana.'},
]

# ============================================================
# CREAR USUARIO
# ============================================================

@login_required
@login_required
def crear_usuario(request):
    # Solo administrador puede acceder
    if not request.user.is_superuser and request.session.get('usuario_rol') != 'Administrador':
        messages.error(request, "No tienes permiso para crear usuarios")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # ✅ Hashear contraseña antes de guardar
            usuario.pass_field = make_password(form.cleaned_data['pass_field'])
            usuario.save()
            messages.success(request, "Usuario creado con éxito")
            return redirect('dashboard')
    else:
        form = UsuarioForm()

    context = {
        'form': form,
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
    }
    return render(request, 'TurnosApp/crear_usuario.html', context)
# ============================================================
# REGISTRO DE USUARIO
# ============================================================

def registro_view(request):
    # Solo permite el acceso si el usuario logueado tiene el rol 'Administrador'
    if request.session.get('usuario_rol') != 'Administrador':
        messages.error(request, 'Solo el administrador puede acceder al registro de usuarios.')
        return redirect('dashboard')

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if Usuarios.objects.filter(rut=rut).exists():
            messages.error(request, 'El RUT ya está registrado.')
        elif Usuarios.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
        else:
            # ✅ Hashear contraseña
            Usuarios.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                pass_field=make_password(password),
                rol=rol
            )
            messages.success(request, 'Usuario registrado con éxito. Ahora puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'TurnosApp/registro.html')
# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    # Limpiar mensajes antiguos solo al entrar por GET
    if request.method == "GET":
        storage = messages.get_messages(request)
        storage.used = True

    if request.method == "POST":
        rut = request.POST.get('rut')
        password = request.POST.get('password')

        # Intentar autenticar como Administrador
        user = authenticate(request, rut_administrador=rut, password=password)
        if user is not None:
            login(request, user)
            request.session['usuario_nombre'] = user.nombre
            request.session['usuario_rol'] = "Administrador"
            messages.success(request, f"Bienvenido {user.nombre} (Administrador)")
            return redirect('dashboard')

        # Si no es administrador, verificar en modelo Usuarios con hash
        try:
            usuario = Usuarios.objects.get(rut=rut)
            if check_password(password, usuario.pass_field):
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_rol'] = usuario.rol
                messages.success(request, f"Bienvenido {usuario.nombre} ({usuario.rol})")
                return redirect('dashboard')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")

    return render(request, 'TurnosApp/login.html')

# ============================================================
# DEMÁS VISTAS (IGUALES)
# ============================================================

def dashboard_view(request):
    if 'usuario_nombre' not in request.session: return redirect('login')
    
    enfermeros_turnos = [
        {'nombre': 'Sofía Rodríguez', 'rol': 'Enfermera', 'turno': 'Mañana', 'estado': 'Activo'},
        {'nombre': 'Carlos Pérez', 'rol': 'Enfermero', 'turno': 'Tarde', 'estado': 'Saliente'},
        {'nombre': 'Ana García', 'rol': 'TENS', 'turno': 'Noche', 'estado': 'Siguiente'},
    ]

    context = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'enfermeros': enfermeros_turnos
    }
    return render(request, 'TurnosApp/dashboard.html', context)


def salas_view(request):
    if 'usuario_nombre' not in request.session: return redirect('login')
    salas_data = [
         {'nombre': 'Sala 101', 'encargado': 'Ana García', 'pacientes': [{'nombre': 'Juan Pérez', 'tareas': ['Administrar medicamentos', 'Monitorear signos vitales']}, {'nombre': 'María González', 'tareas': ['Cura de herida', 'Asistencia en higiene']}]},
         {'nombre': 'Sala 102', 'encargado': 'Carlos Soto', 'pacientes': [{'nombre': 'Pedro Pascal', 'tareas': ['Administrar medicamentos']}]},
    ]
    context = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'salas': salas_data
    }
    return render(request, 'TurnosApp/salas.html', context)


def pacientes_view(request):
    if 'usuario_nombre' not in request.session: return redirect('login')
    context = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'pacientes': PACIENTES_DATA
    }
    return render(request, 'TurnosApp/pacientes.html', context)

def ficha_paciente_view(request, id_paciente):
    if 'usuario_nombre' not in request.session:
        return redirect('login')

    paciente = next((p for p in PACIENTES_DATA if p['id'] == id_paciente), None)
    covid_data = None
    alerta_epidemiologica = None

    if paciente:
        pais = paciente.get("pais", "")
        fiebre = paciente.get("fiebre", False)
        contagio = paciente.get("contagio", False)
        diagnostico = paciente.get("diagnostico", "").lower()

        diagnosticos_respiratorios = ["covid", "neumonía", "bronquitis", "asma", "neumonia", "sars", "influenza"]

        mostrar_covid = fiebre or contagio or diagnostico in diagnosticos_respiratorios

        if pais and mostrar_covid:
            try:
                url = f"https://disease.sh/v3/covid-19/historical/{pais}?lastdays=1"
                response = requests.get(url)
                data = response.json()

                if "timeline" in data:
                    covid_data = {
                        "pais": pais,
                        "casos": list(data["timeline"]["cases"].values())[0],
                        "muertes": list(data["timeline"]["deaths"].values())[0],
                        "recuperados": list(data["timeline"]["recovered"].values())[0],
                    }

                    if covid_data["casos"] > 2000:
                        alerta_epidemiologica = f"⚠️ Aumento elevado de casos COVID-19 en {pais}"
            except Exception as e:
                print(">>> ERROR API:", e)

    return render(request, "TurnosApp/ficha_paciente.html", {
        "paciente": paciente,
        "covid_data": covid_data,
        "alerta_epidemiologica": alerta_epidemiologica,
        "usuario_nombre": request.session.get("usuario_nombre"),
        "usuario_rol": request.session.get("usuario_rol"),
    })



def personal_view(request):
    if 'usuario_nombre' not in request.session: return redirect('login')
    context = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
    }
    return render(request, 'TurnosApp/personal.html', context)


def horarios_view(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    usuario_nombre = request.session.get("usuario_nombre")
    usuario_rol = (request.session.get("usuario_rol") or "").strip().lower()

    horarios = []
    simulado = False

    # 👑 ADMINISTRADOR: ve todos los horarios simulados
    if usuario_rol == "administrador":
        horarios = [
            {'nombre': 'Sofía Rodríguez', 'rol': 'Enfermera', 'dia_semana': 'Lunes', 'fecha': '2025-11-10', 'hora_inicio': '08:00', 'hora_fin': '16:00', 'sala': 'Sala 101'},
            {'nombre': 'Carlos Pérez', 'rol': 'Enfermero', 'dia_semana': 'Martes', 'fecha': '2025-11-11', 'hora_inicio': '16:00', 'hora_fin': '00:00', 'sala': 'Sala 102'},
            {'nombre': 'Ana García', 'rol': 'TENS', 'dia_semana': 'Miércoles', 'fecha': '2025-11-12', 'hora_inicio': '08:00', 'hora_fin': '16:00', 'sala': 'Sala 103'},
            {'nombre': 'Pedro Soto', 'rol': 'TENS', 'dia_semana': 'Jueves', 'fecha': '2025-11-13', 'hora_inicio': '16:00', 'hora_fin': '00:00', 'sala': 'Sala 104'},
            {'nombre': 'Laura Díaz', 'rol': 'Enfermera', 'dia_semana': 'Viernes', 'fecha': '2025-11-14', 'hora_inicio': '08:00', 'hora_fin': '15:00', 'sala': 'Sala 105'},
        ]
        simulado = True

    # 👩‍⚕️ ENFERMEROS: ven solo sus horarios
    elif usuario_rol == "enfermero":
        horarios = [
            {'nombre': usuario_nombre, 'rol': 'Enfermero', 'dia_semana': 'Lunes', 'fecha': '2025-11-10', 'hora_inicio': '08:00', 'hora_fin': '16:00', 'sala': 'Sala 101'},
            {'nombre': usuario_nombre, 'rol': 'Enfermero', 'dia_semana': 'Miércoles', 'fecha': '2025-11-12', 'hora_inicio': '16:00', 'hora_fin': '00:00', 'sala': 'Sala 103'},
        ]
        simulado = True

    # 👨‍⚕️ TENS: ven solo sus horarios
    elif usuario_rol == "tens":
        horarios = [
            {'nombre': usuario_nombre, 'rol': 'TENS', 'dia_semana': 'Martes', 'fecha': '2025-11-11', 'hora_inicio': '08:00', 'hora_fin': '16:00', 'sala': 'Sala 201'},
            {'nombre': usuario_nombre, 'rol': 'TENS', 'dia_semana': 'Jueves', 'fecha': '2025-11-13', 'hora_inicio': '16:00', 'hora_fin': '00:00', 'sala': 'Sala 202'},
        ]
        simulado = True

    else:
        messages.info(request, "No tienes horarios designados por el momento.")

    context = {
        "usuario_nombre": usuario_nombre,
        "usuario_rol": request.session.get("usuario_rol"),
        "horarios": horarios,
        "simulado": simulado,
    }

    return render(request, "TurnosApp/horarios.html", context)


# ============================================================
# REPORTES Y LOGOUT (idénticos a los tuyos)
# ============================================================

def reportes_view(request):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    if request.method == "POST":
        contenido = request.POST.get("contenido", "").strip()
        if contenido:
            nuevo = {
                "id": str(uuid.uuid4()),
                "autor": request.session.get("usuario_nombre"),
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "contenido": contenido,
            }
            REPORTES_DATA.insert(0, nuevo)
            messages.success(request, "Reporte agregado con éxito.")
        return redirect("reportes")

    context = {
        "usuario_nombre": request.session.get("usuario_nombre"),
        "usuario_rol": request.session.get("usuario_rol"),
        "reportes": REPORTES_DATA,
    }
    return render(request, "TurnosApp/reportes.html", context)


def reporte_editar_view(request, reporte_id):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    reporte = next((r for r in REPORTES_DATA if r["id"] == reporte_id), None)
    if not reporte:
        messages.error(request, "El reporte no fue encontrado.")
        return redirect("reportes")

    autor_actual = request.session.get("usuario_nombre")
    rol_actual = (request.session.get("usuario_rol") or "").strip().capitalize()

    if reporte["autor"] != autor_actual and rol_actual != "Administrador":
        messages.error(request, "No tienes permiso para editar este reporte.")
        return redirect("reportes")

    if request.method == "POST":
        nuevo_contenido = request.POST.get("contenido", "").strip()
        if nuevo_contenido:
            reporte["contenido"] = nuevo_contenido
            messages.success(request, "Reporte actualizado con éxito.")
        return redirect("reportes")

    return render(request, "TurnosApp/reporte_form.html", {
        "reporte": reporte,
        "usuario_nombre": autor_actual,
        "usuario_rol": rol_actual,
    })


def reporte_eliminar_view(request, reporte_id):
    if "usuario_nombre" not in request.session:
        return redirect("login")

    reporte = next((r for r in REPORTES_DATA if r["id"] == reporte_id), None)
    if not reporte:
        messages.error(request, "El reporte no fue encontrado.")
        return redirect("reportes")

    autor_actual = request.session.get("usuario_nombre")
    rol_actual = (request.session.get("usuario_rol") or "").strip().capitalize()

    if reporte["autor"] != autor_actual and rol_actual != "Administrador":
        messages.error(request, "No tienes permiso para eliminar este reporte.")
        return redirect("reportes")

    if request.method == "POST":
        REPORTES_DATA.remove(reporte)
        messages.success(request, "Reporte eliminado con éxito.")
        return redirect("reportes")

    return render(request, "TurnosApp/reporte_confirm_delete.html", {
        "reporte": reporte,
        "usuario_nombre": autor_actual,
        "usuario_rol": rol_actual,
    })


def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    return redirect('login')
