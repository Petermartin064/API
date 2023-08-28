from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        Admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" or Admin_permission
