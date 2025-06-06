# project/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Importaciones necesarias para drf_yasg (Swagger/OpenAPI)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuramos el “schema view” para Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="VisionAI API",
      default_version='v1',
      description="Documentación de la API VisionAI – Administración de Facturas y Documentos",
      terms_of_service="https://www.tu-dominio.com/terms/",
      contact=openapi.Contact(email="soporte@tu-dominio.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 1) Página de administración de Django
    path('admin/', admin.site.urls),

    # 2) Rutas de tu aplicación “VisionAI” (API REST) bajo /api/
    path('api/', include('VisionAI.urls')),  # Aquí están: facturas/, facturas/<id>/, facturas/<id>/documentos/

    # 3) Endpoints de Swagger/OpenAPI
    #    - swagger.json / swagger.yaml  (para el esquema “sin UI”)
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    #    - swagger/  (interfaz Swagger UI)
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    #    - redoc/  (interfaz Redoc)
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

# Si sirves archivos estáticos/media en desarrollo (opcional):
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

