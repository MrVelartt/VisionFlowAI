from rest_framework import serializers
from .models import Factura, DocumentoFactura

class DocumentoFacturaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo DocumentoFactura.
    Devuelve id, URL del archivo y fecha de subida.
    """
    class Meta:
        model = DocumentoFactura
        fields = [
            'id',
            'archivo',
            'uploaded_at',
        ]
        read_only_fields = ['id', 'uploaded_at']


class FacturaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Factura.
    Incluye un campo ‘documentos’ que anida todos los archivos asociados.
    """
    documentos = DocumentoFacturaSerializer(many=True, read_only=True)

    class Meta:
        model = Factura
        fields = [
            'id',
            'cliente',
            'correo_electronico',
            'descripcion',
            'uploaded_at',
            'documentos',
        ]
        read_only_fields = ['id', 'uploaded_at', 'documentos']