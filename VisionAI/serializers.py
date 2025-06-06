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
    Incluye:
      - campo 'documentos' que anida todos los archivos asociados,
      - campo 'resumen_excel' que expone la URL del Excel generado (si existe).
    """
    documentos = DocumentoFacturaSerializer(many=True, read_only=True)
    resumen_excel = serializers.FileField(read_only=True)

    class Meta:
        model = Factura
        fields = [
            'id',
            'cliente',
            'correo_electronico',
            'descripcion',
            'uploaded_at',
            'documentos',
            'resumen_excel',    # Se agregó para exponer la URL del Excel
        ]
        read_only_fields = ['id', 'uploaded_at', 'documentos', 'resumen_excel']


class FacturaCreateWithDocsSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una Factura y sus Documentos en un solo paso.
    El campo 'archivos' es write_only y se usará para subir uno o varios archivos.
    """
    archivos = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        allow_empty=False,
        help_text="Lista de archivos que se asociarán a esta factura"
    )

    class Meta:
        model = Factura
        fields = [
            'cliente',
            'correo_electronico',
            'descripcion',
            'archivos',   # write_only
        ]

    def create(self, validated_data):
        # 1. Extraer la lista de archivos
        archivos = validated_data.pop('archivos')
        # 2. Crear la factura con los campos restantes
        factura = Factura.objects.create(**validated_data)
        # 3. Crear un DocumentoFactura por cada archivo
        for archivo in archivos:
            DocumentoFactura.objects.create(factura=factura, archivo=archivo)
        return factura

    def to_representation(self, instance):
        """
        Al devolver la factura recién creada, devolvemos la misma estructura
        que FacturaSerializer (incluyendo 'documentos' y 'resumen_excel').
        """
        return FacturaSerializer(instance, context=self.context).data
