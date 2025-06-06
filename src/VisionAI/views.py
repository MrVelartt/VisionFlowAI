# VisionAI/views.py

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Factura, DocumentoFactura
from .serializers import (
    FacturaSerializer,
    FacturaCreateWithDocsSerializer,
    DocumentoFacturaSerializer,
)


class FacturaListCreateAPIView(APIView):
    """
    GET  -> Lista todas las facturas con sus documentos anidados.
    POST -> Crea una nueva factura y sube todos los archivos a la vez:
            espera multipart/form-data con:
             - cliente (string)
             - correo_electronico (string)
             - descripcion (string, opcional)
             - archivos[] (uno o varios archivos)
    """
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Crear factura y subir todos sus documentos de una vez.",
        manual_parameters=[
            openapi.Parameter(
                name='cliente',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Nombre completo del cliente",
                required=True,
                example="Juan Camilo Velásquez"
            ),
            openapi.Parameter(
                name='correo_electronico',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Correo electrónico del cliente",
                required=True,
                example="cliente@ejemplo.com"
            ),
            openapi.Parameter(
                name='descripcion',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Descripción breve de la factura (opcional)",
                required=False,
                example="Documentación exógena junio 2025"
            ),
            openapi.Parameter(
                name='archivos',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE),
                description="Lista de archivos de la factura (archivos[])",
                required=True,
            ),
        ],
        request_body=None,
        responses={
            201: openapi.Response(
                description="Factura creada con documentos",
                schema=FacturaSerializer()
            ),
            400: "Errores de validación"
        }
    )
    def post(self, request):
        serializer = FacturaCreateWithDocsSerializer(data=request.data)
        if serializer.is_valid():
            factura = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Listar todas las facturas con sus documentos anidados.",
        responses={200: FacturaSerializer(many=True)}
    )
    def get(self, request):
        facturas = Factura.objects.prefetch_related('documentos').all().order_by('-uploaded_at')
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FacturaRetrieveAPIView(APIView):
    """
    GET -> Devuelve los datos de una factura específica (incluyendo sus documentos).
    """
    @swagger_auto_schema(
        operation_description="Obtener datos de una factura específica con sus documentos.",
        responses={
            200: FacturaSerializer(),
            404: "Factura no encontrada"
        }
    )
    def get(self, request, id):
        try:
            factura = Factura.objects.prefetch_related('documentos').get(id=id)
        except Factura.DoesNotExist:
            return Response({"detail": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FacturaSerializer(factura)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentoFacturaCreateAPIView(APIView):
    """
    POST -> Recibe uno o varios archivos y los asocia a la Factura indicada por factura_id.
    - En el formulario, el campo 'archivos' puede contener múltiples ficheros.
    """
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Subir uno o varios documentos a una factura existente.",
        manual_parameters=[
            openapi.Parameter(
                name='archivos',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE),
                description="Lista de documentos para adjuntar a la factura",
                required=True
            ),
        ],
        request_body=None,
        responses={
            201: DocumentoFacturaSerializer(many=True),
            400: "No se enviaron archivos o error de validación",
            404: "Factura no encontrada"
        }
    )
    def post(self, request, factura_id):
        try:
            factura = Factura.objects.get(id=factura_id)
        except Factura.DoesNotExist:
            return Response({"detail": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        archivos = request.FILES.getlist('archivos')
        if not archivos:
            return Response(
                {"detail": "Debes enviar al menos un archivo en el campo 'archivos'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nuevos_documentos = []
        for f in archivos:
            doc = DocumentoFactura.objects.create(factura=factura, archivo=f)
            nuevos_documentos.append(doc)

        serializer = DocumentoFacturaSerializer(nuevos_documentos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FacturaReporteAPIView(APIView):
    """
    GET -> Devuelve (o redirige) la URL para descargar el Excel generado de la factura.
    """
    @swagger_auto_schema(
        operation_description="Obtener URL del reporte Excel de la factura.",
        responses={
            200: "JSON con clave 'url' al archivo Excel",
            404: "Factura no encontrada o Excel no generado aún"
        }
    )
    def get(self, request, id):
        try:
            factura = Factura.objects.get(id=id)
        except Factura.DoesNotExist:
            return Response({"detail": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if not factura.resumen_excel:
            return Response(
                {"detail": "El Excel aún no ha sido generado. Intenta nuevamente en unos instantes."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retornar la URL al Excel (ya sea pública o firmada por AWS S3)
        url = factura.resumen_excel.url
        return Response({"url": url}, status=status.HTTP_200_OK)
