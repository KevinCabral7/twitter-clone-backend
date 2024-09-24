"""
ASGI config for Api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import twitter.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Api.settings')

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(twitter.routing.websocket_urlpatterns))
        ),
    }
)
