from django.urls import path
from .views import (
    FacturaListCreateAPIView,
    FacturaRetrieveAPIView,
    DocumentoFacturaCreateAPIView,
)

urlpatterns = [
    # Listar y crear facturas: GET /api/facturas/   ,  POST /api/facturas/
    path('facturas/', FacturaListCreateAPIView.as_view(), name='factura-list-create'),
    
    # Obtener una factura por ID: GET /api/facturas/<id>/
    path('facturas/<int:id>/', FacturaRetrieveAPIView.as_view(), name='factura-retrieve'),

    # Subir uno o varios documentos a la factura indicada (campo "archivos" en form-data)
    # POST /api/facturas/<factura_id>/documentos/
    path(
        'facturas/<int:factura_id>/documentos/',
        DocumentoFacturaCreateAPIView.as_view(),
        name='documento-factura-create'
    ),
]