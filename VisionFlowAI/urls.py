from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de la app VisionAI bajo /api/
    path('api/', include('VisionAI.urls')),
]

