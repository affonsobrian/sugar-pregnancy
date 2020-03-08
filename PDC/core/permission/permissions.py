from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsDoctor(IsAuthenticated):
    def has_permission(self, request, view):
        authenticated = super(IsDoctor, self).has_permission(request, view)
        if not authenticated:
            return False
        return request.user.is_doctor()


class IsPatient(IsAuthenticated):
    def has_permission(self, request, view):
        authenticated = super(IsPatient, self).has_permission(request, view)
        if not authenticated:
            return False
        return request.user.is_patient()


class IsAuthenticatedOrWriteOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in ['POST'] or
            request.user and
            request.user.is_authenticated
        )


class ChangeItSelfOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.method in ('POST',) or
            (request.user and
             request.user.is_authenticated and
             obj.user == request.user)
        )