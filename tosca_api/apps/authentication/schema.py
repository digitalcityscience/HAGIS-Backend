"""drf-spectacular integration for the Keycloak DRF authenticator.

Without this extension spectacular cannot describe KeycloakTokenAuthentication
and emits a W001 warning for every view that uses the default auth classes.
"""

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KeycloakTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "tosca_api.apps.authentication.backends.KeycloakTokenAuthentication"
    name = "bearerAuth"

    def get_security_definition(self, auto_schema):
        return {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
