import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { ItemDocName } from './item-doc-name/item-doc-name';
import { ItemStatus } from './item-status/item-status';
import { ItemActions } from './item-actions/item-actions';
import { Document } from '@core/models';

@Component({
  selector: 'app-documents-table',
  imports: [ItemDocName, ItemStatus, ItemActions],
  templateUrl: './documents-table.html',
  styleUrl: './documents-table.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DocumentsTable {
  readonly documents = input.required<Document[]>();

  protected onDownload(doc: Document): void {
    // Realizar la descarga
  }

  protected onView(doc: Document): void {
    // Ver el documento
  }

  protected onRetry(doc: Document): void {
    // Reintentar la descarga
  }
}
