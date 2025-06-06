# VisionAI/urls.py

from django.urls import path
from .views import (
    FacturaListCreateAPIView,
    FacturaRetrieveAPIView,
    DocumentoFacturaCreateAPIView,
    FacturaReporteAPIView,
)

urlpatterns = [
    # 1) Listar y crear facturas:
    #    GET  /api/facturas/
    #    POST /api/facturas/
    path('facturas/', FacturaListCreateAPIView.as_view(), name='factura-list-create'),

    # 2) Detalle de factura (incluye documentos y, si existe, la URL de Excel):
    #    GET /api/facturas/<id>/
    path('facturas/<int:id>/', FacturaRetrieveAPIView.as_view(), name='factura-retrieve'),

    # 3) Subir documentos a una factura ya existente:
    #    POST /api/facturas/<factura_id>/documentos/
    path(
        'facturas/<int:factura_id>/documentos/',
        DocumentoFacturaCreateAPIView.as_view(),
        name='documento-factura-create'
    ),

    # 4) Obtener URL para descargar el Excel generado:
    #    GET /api/facturas/<id>/reporte/
    path(
        'facturas/<int:id>/reporte/',
        FacturaReporteAPIView.as_view(),
        name='factura-reporte'
    ),
]
