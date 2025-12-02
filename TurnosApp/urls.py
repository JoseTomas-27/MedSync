from django.contrib import admin
from django.urls import path
from TurnosApp import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),  # opcional, por si usas ambas
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('salas/', views.salas_view, name='salas'),
    path('pacientes/', views.pacientes_view, name='pacientes'),
    path('pacientes/ficha/<int:id_paciente>/', views.ficha_paciente_view, name='ficha_paciente'),
    path('personal/', views.personal_view, name='personal'),
    path('horarios/', views.horarios_view, name='horarios'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('reportes/editar/<str:reporte_id>/', views.reporte_editar_view, name='reporte_editar'),
    path('reportes/eliminar/<str:reporte_id>/', views.reporte_eliminar_view, name='reporte_eliminar'),
    path('admin/', admin.site.urls),
]


