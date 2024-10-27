from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.conf import settings
from keycloak import KeycloakOpenID

from .models import StatelessUser

class KeycloakTokenAuthentication(BaseAuthentication):
    """
    Simple Keycloak token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'
    model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_SERVER_URL,
                                 client_id=settings.CLIENT_ID,
                                 realm_name=settings.REALM_NAME,
                                 client_secret_key=settings.CLIENT_SECRET_KEY)

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
            access_token_introspect = self.keycloak_openid.introspect(token)

        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        
        return (StatelessUser(access_token_introspect), token)

    def authenticate_header(self, request):
        return self.keyword