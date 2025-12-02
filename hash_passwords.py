# hash_passwords.py
from django.contrib.auth.hashers import make_password
from TurnosApp.models import Usuarios

def run():
    usuarios = Usuarios.objects.all()
    total_actualizados = 0

    for usuario in usuarios:
        password = usuario.pass_field
        # Solo si no está hasheada (no comienza con "pbkdf2_")
        if password and not password.startswith("pbkdf2_"):
            usuario.pass_field = make_password(password)
            usuario.save()
            total_actualizados += 1
            print(f"✅ Contraseña hasheada para {usuario.nombre} ({usuario.rut})")

    if total_actualizados == 0:
        print("⚠️ No se encontraron contraseñas sin hash.")
    else:
        print(f"✅ {total_actualizados} contraseñas convertidas correctamente.")
