"""
ASGI config for courtside_analytics project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# courtside_analytics/asgi.py
import os
from django.core.asgi import get_asgi_application

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'courtside_analytics.settings.development')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()
