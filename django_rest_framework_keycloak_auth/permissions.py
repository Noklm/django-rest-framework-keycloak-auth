from rest_framework import permissions

class HasKeycloakRoles(permissions.BasePermission):
    """
    Global permission to authorise only Keycloak roles
    """
    def has_permission(self, request, view):

        if any(item in view.keycloak_roles for item in request.user.roles):
            return True

        return False
    # """
    # Object-level permission to only allow keycloak roles.
    # """

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     # Instance must have an attribute named `owner`.
    #     return obj.owner == request.user
    
