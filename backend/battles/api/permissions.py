from rest_framework import permissions


class IsTheTrainerOfTheTeam(permissions.BasePermission):

    message = "This user isn't the trainer of this team."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if str(obj.trainer) == str(request.user):
            return True
        return False
