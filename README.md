# Keycloak authentication for Django REST framework


django-rest-framework-keycloak-auth is a Django app to use Single sign-on using Keycloak.
Users aren't now managed by Keycloak. This app is based on djangorestframework

## Dependencies
1. [django](https://www.djangoproject.com/)
2. [djangorestframework](https://www.django-rest-framework.org/)
3. [python-keycloak](https://github.com/marcospereirampj/python-keycloak)
## Quick start

In settings.py, 
1.  add "keycloak-auth" to your `INSTALLED_APPS` setting like this:

```py
    INSTALLED_APPS = [
        ...,
        "django_rest_framework_keycloak_auth",
    ]
```

2. add your keycloak client credentials:
```py
import os

...

KEYCLOAK_SERVER_URL = os.environ['KEYCLOAK_SERVER_URL']
CLIENT_ID = os.environ['CLIENT_ID']
REALM_NAME = os.environ['REALM_NAME']
CLIENT_SECRET_KEY = os.environ['CLIENT_SECRET_KEY']
```

2. Use the Keycloak token authentication class as default
```py
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'django_rest_framework_keycloak_auth.authentication.KeycloakTokenAuthentication',
    ],
}
```

## View permission based on Keycloak roles
This method is using Django [REST Framework permissions system](https://www.django-rest-framework.org/api-guide/permissions/) In your views.py:
```py
from django_rest_framework_keycloak_auth.permissions import HasKeycloakRoles

class MyView(viewsets.ModelViewSet):
    """
    This ViewSet is globally accessed by Keycloak user with manage-account role.
    """
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [HasKeycloakRoles]
    keycloak_roles = ["manage-account"]
```

## Build and install from sources

```sh
python -m build

# In venv
python -m pip install dist/django_rest_framework_keycloak_auth-0.1.0.tar.gz
```