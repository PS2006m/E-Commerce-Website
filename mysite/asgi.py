import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapp.routing  # ✅ Ensure this matches your app name!

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # ✅ Check the project name!

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns  # ✅ Ensure this is correct
        )
    ),
})
