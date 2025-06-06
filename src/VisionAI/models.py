# VisionAI/models.py

from django.db import models


class Factura(models.Model):
    cliente = models.CharField(
        max_length=255,
        help_text="Nombre completo del cliente"
    )
    correo_electronico = models.EmailField(
        help_text="Correo electrónico del cliente"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción corta o anotaciones sobre la factura"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # — Ajuste: campo para guardar el Excel generado tras procesar documentos —
    resumen_excel = models.FileField(
        upload_to='resumenes/',
        blank=True,
        null=True,
        help_text="Archivo Excel con los datos extraídos de la factura"
    )

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente}"


class DocumentoFactura(models.Model):
    factura = models.ForeignKey(
        Factura,
        related_name='documentos',
        on_delete=models.CASCADE
    )
    archivo = models.FileField(
        upload_to='facturas/',
        help_text="Archivo de la factura (PDF, JPG, PNG, …)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc-{self.id} de Factura#{self.factura_id}"
