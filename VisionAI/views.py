from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Factura, DocumentoFactura
from .serializers import FacturaSerializer, DocumentoFacturaSerializer

class FacturaListCreateAPIView(APIView):
    """
    GET  -> Lista todas las facturas con sus documentos anidados.
    POST -> Crea una nueva factura (sin documentos).
    """
    def get(self, request):
        facturas = Factura.objects.prefetch_related('documentos').all().order_by('-uploaded_at')
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FacturaSerializer(data=request.data)
        if serializer.is_valid():
            factura = serializer.save()
            return Response(FacturaSerializer(factura).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacturaRetrieveAPIView(APIView):
    """
    GET -> Devuelve los datos de una factura específica (incluyendo sus documentos).
    """
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
    - En el formulario, el campo para los archivos debe llamarse "archivos" y puede contener múltiples ficheros.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, factura_id):
        # 1. Verificar que la factura exista
        try:
            factura = Factura.objects.get(id=factura_id)
        except Factura.DoesNotExist:
            return Response({"detail": "Factura no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Obtener la lista de archivos del campo 'archivos'
        archivos = request.FILES.getlist('archivos')
        if not archivos:
            return Response(
                {"detail": "Debes enviar al menos un archivo en el campo 'archivos'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Crear una instancia de DocumentoFactura por cada archivo
        nuevos_documentos = []
        for f in archivos:
            doc = DocumentoFactura.objects.create(factura=factura, archivo=f)
            nuevos_documentos.append(doc)

        # 4. Serializar y devolver los documentos creados
        serializer = DocumentoFacturaSerializer(nuevos_documentos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
