from rest_framework.permissions import BasePermission


def has_user_type(user, user_type):
    print(user.is_authenticated, user.user_type, user_type)
    print(user.is_authenticated and int(user.user_type) >= int(user_type))
    return user.is_authenticated and int(user.user_type) >= int(user_type)


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return has_user_type(request.user, "0")


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return has_user_type(request.user, "1")


class IsGuidance(BasePermission):
    def has_permission(self, request, view):
        return has_user_type(request.user, "2")


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_user_type(request.user, "3")
