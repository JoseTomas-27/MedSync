# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=15, blank=True, unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    correo = models.CharField(unique=True, max_length=80, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=100, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    rol = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuarios'


class Tareas(models.Model):
    id_tarea = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True)
    descripcion = models.TextField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = 'tareas'


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, rut_administrador, email, nombre, password=None):
        if not rut_administrador:
            raise ValueError('El RUT debe ser proporcionado')
        user = self.model(
            rut_administrador=rut_administrador,
            email=self.normalize_email(email),
            nombre=nombre,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut_administrador, email, nombre, password=None):
        user = self.create_user(
            rut_administrador=rut_administrador,
            email=email,
            nombre=nombre,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Administrador(AbstractBaseUser, PermissionsMixin):
    rut_administrador = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'rut_administrador'
    REQUIRED_FIELDS = ['email', 'nombre']

    objects = UserManager()
    
    class Meta:
        db_table = 'administrador'

    def __str__(self):
        return self.nombre or self.rut_administrador


class Enfermeros(models.Model):
    rut_enfermero = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        db_table = 'enfermeros'


class HistorialMedico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', blank=True, null=True)
    diagnostico = models.CharField(max_length=200, blank=True, null=True)
    examenes_previos = models.CharField(db_column='Examenes_Previos', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    examenes_pendientes = models.CharField(db_column='Examenes_pendientes', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'historial_medico'


class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    dia_semana = models.CharField(max_length=9, blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    rut_tens = models.ForeignKey('Tens', models.DO_NOTHING, db_column='rut_tens', blank=True, null=True)
    rut_enfermero = models.ForeignKey(Enfermeros, models.DO_NOTHING, db_column='rut_enfermero', blank=True, null=True)

    class Meta:
        db_table = 'horarios'


class Pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=4, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    id_sala = models.ForeignKey('Salas', models.DO_NOTHING, db_column='id_sala', blank=True, null=True)

    class Meta:
        db_table = 'pacientes'


class Salas(models.Model):
    id_sala = models.AutoField(primary_key=True)
    capacidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'salas'


class Tens(models.Model):
    rut_tens = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        db_table = 'tens'


class Turnos(models.Model):
    id_turno = models.AutoField(primary_key=True)
    fecha_turno = models.DateField(blank=True, null=True)
    dia_semana = models.CharField(max_length=9, blank=True, null=True)
    hora_turno = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'turnos'
