# VisionAI/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Factura
from .utils import procesar_factura_ocr_y_generar_excel

@receiver(post_save, sender=Factura)
def factura_post_save_handler(sender, instance, created, **kwargs):
    """
    Al crear una nueva Factura, disparamos el procesamiento en cuanto termine la transacción.
    Esto hará:
      - Leer todos los documentos asociados (DocumentoFactura).
      - Ejecutar OCR sobre cada archivo.
      - Crear un Excel con los datos.
      - Guardar el Excel en el campo resumen_excel (que subirá a S3).
    """
    if created:
        # Asegurarse de ejecutar la lógica AFTER de que la factura y sus documentos estén en DB
        transaction.on_commit(lambda: procesar_factura_ocr_y_generar_excel(instance))
