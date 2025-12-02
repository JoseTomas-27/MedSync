from rest_framework.permissions import BasePermission


class IsAdminUserSession(BasePermission):
    """
    Permite acceso solo si el usuario tiene rol de administrador en la sesión.
    """
    def has_permission(self, request, view):
        return request.session.get('usuario_rol') == 'Administrador'
