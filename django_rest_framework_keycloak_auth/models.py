from collections.abc import Iterable

from django.contrib.auth.models import Group, Permission, _user_get_permissions, _user_has_perm, _user_has_module_perms
from django.db.models.manager import EmptyManager

class StatelessUser:
    
    id = None
    pk = None
    username = ""
    is_staff = False
    is_active = False
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def __init__(self, access_token, *args, **kwargs):
        self.access_token = access_token
        self.id = access_token['sub']
        self.sub = access_token['sub']
        self.username = access_token['preferred_username']
        self.roles = access_token['resource_access']['account']['roles']
        self.is_active = access_token.get('active', False)
        self.is_authenticated = True
        self.is_anonymous = False

    def __str__(self):
        return self.username

    def __eq__(self, other):
        return self.sub == other.sub

    def __hash__(self):
        return hash(self.sub())

    def __int__(self):
        raise TypeError(
            "Cannot cast StatelessUser to int. Are you trying to use it in place of "
            "User?"
        )

    def save(self):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for StatelessUser."
        )

    def delete(self):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for StatelessUser."
        )

    def set_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for StatelessUser."
        )

    def check_password(self, raw_password):
        raise NotImplementedError(
            "Django doesn't provide a DB representation for StatelessUser."
        )

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        if not isinstance(perm_list, Iterable) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    def get_username(self):
        return self.username

    