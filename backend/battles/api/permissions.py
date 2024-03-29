from rest_framework import permissions


class IsTrainerOfTeam(permissions.BasePermission):

    message = "This user isn't the trainer of this team."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if str(obj.trainer.email) == str(request.user.email):
            return True
        return False
