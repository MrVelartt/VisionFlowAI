import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { SimpleHeader } from '@shared/components';
import { DocumentsFilters, DocumentsTable } from './components';
import { Document } from '@core/models';

@Component({
  selector: 'app-download-center',
  imports: [SimpleHeader, DocumentsTable, DocumentsFilters],
  templateUrl: './download-center.html',
  styleUrl: './download-center.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DownloadCenter {
  protected readonly documents = signal<Document[]>([
    {
      id: '1',
      type: 'pdf',
      name: 'Factura 001.pdf',
      upload_date: 'Junio 15, 2024',
      status: {
        key: 'processed',
        value: 'Procesado',
      },
    },
    {
      id: '2',
      type: 'docx',
      name: 'Contrato Servicio.docx',
      upload_date: 'Mayo 20, 2024',
      status: {
        key: 'pending',
        value: 'Pendiente',
      },
    },
    {
      id: '3',
      type: 'xlsx',
      name: 'Reporte Ventas Q1.xlsx',
      upload_date: 'Abril 10, 2024',
      status: {
        key: 'processed',
        value: 'Procesado',
      },
    },
    {
      id: '4',
      type: 'pdf',
      name: 'Recibo de Pago.pdf',
      upload_date: 'Marzo 5, 2024',
      status: {
        key: 'error',
        value: 'Error',
      },
    },
    {
      id: '5',
      type: 'xlsx',
      name: 'Presentación Anual.xlsx',
      upload_date: 'Febrero 28, 2024',
      status: {
        key: 'processed',
        value: 'Procesado',
      },
    },
    {
      id: '6',
      type: 'pdf',
      name: 'Factura 002.pdf',
      upload_date: 'Enero 12, 2024',
      status: {
        key: 'pending',
        value: 'Pendiente',
      },
    },
  ]);
}
