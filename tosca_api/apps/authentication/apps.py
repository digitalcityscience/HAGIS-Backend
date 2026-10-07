from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tosca_api.apps.authentication"
    label = "tosca_authentication"

    def ready(self):
        # Registers the OpenAPI extension for KeycloakTokenAuthentication.
        from . import schema  # noqa: F401
