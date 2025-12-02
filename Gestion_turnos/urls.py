from django.contrib import admin
from django.urls import path, include
from TurnosApp import views

urlpatterns = [
    # Autenticación
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Paneles Principales
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('salas/', views.salas_view, name='salas'),
    path('pacientes/', views.pacientes_view, name='pacientes'),
    path('pacientes/ficha/<int:id_paciente>/', views.ficha_paciente_view, name='ficha_paciente'),
    path('personal/', views.personal_view, name='personal'),
    path('horarios/', views.horarios_view, name='horarios'),
    path('', include('TurnosApp.urls')),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),

    # --- CRUD DE REPORTES (RUTAS CORREGIDAS) ---
    path('reportes/', views.reportes_view, name='reportes'),
    # Usamos <str:reporte_id> para que coincida con los IDs ('reporte-1-sofia')
    path('reportes/editar/<str:reporte_id>/', views.reporte_editar_view, name='reporte_editar'),
    path('reportes/eliminar/<str:reporte_id>/', views.reporte_eliminar_view, name='reporte_eliminar'),

    # Admin
    path('admin/', admin.site.urls),
]