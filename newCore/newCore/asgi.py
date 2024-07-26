# """
# ASGI config for newCore project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.auth import AuthMiddlewareStack
# from home.routing import websocket_urlpatterns
# from channels.security.websocket import AllowedHostsOriginValidator
# import home.routing



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newCore.settings')


# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
                
#                 URLRouter(
                    
#                     websocket_urlpatterns
                    
#                         )
                        
#                                )
#         ),
   
# })



import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
# from home.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newCore.settings')

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         )
#     ),
# })
