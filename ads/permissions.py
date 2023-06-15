from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем подборки"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "author"):
            owner = obj.author
        else:
            raise Exception("Неверно применен permissions")

        if request.user == owner:
            return True


class IsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == [UserRole.ADMIN, UserRole.MODERATOR]:
            return True
