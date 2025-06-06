from django.contrib import admin
from .models import Factura, DocumentoFactura

class DocumentoFacturaInline(admin.TabularInline):
    """
    Inline para que, al editar o crear una Factura, puedas añadir varios documentos
    (DocumentoFactura) directamente en la misma página.
    """
    model = DocumentoFactura
    extra = 1               # Número inicial de filas vacías para subir archivos
    readonly_fields = ('uploaded_at',)
    fields = ('archivo', 'uploaded_at')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'correo_electronico', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    search_fields = ('cliente', 'correo_electronico')
    inlines = [DocumentoFacturaInline]  # Muestra el inline de documentos en la página de Factura


@admin.register(DocumentoFactura)
class DocumentoFacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'archivo', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    list_filter = ('factura',)