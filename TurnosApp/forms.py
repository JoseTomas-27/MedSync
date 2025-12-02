from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    rol = forms.ChoiceField(choices=Usuarios.rol, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Usuarios.objects.create(usuario=user, rol=self.cleaned_data['rol'])
        return user

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['rut', 'nombre', 'apellido', 'correo', 'pass_field', 'rol']
        widgets = {
            'pass_field': forms.PasswordInput(),
        }