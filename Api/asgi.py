"""
ASGI config for Api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import twitter.routing 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Api.settings')


try:
    django.setup()
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
except Exception as e:
    print(f"Error setting up Django: {e}")


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(twitter.routing.websocket_urlpatterns))
        ),
    }
)
