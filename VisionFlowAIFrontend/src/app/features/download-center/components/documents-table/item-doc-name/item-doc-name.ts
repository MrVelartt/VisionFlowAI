import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { Document } from '@core/models';

@Component({
  selector: 'app-item-doc-name',
  imports: [],
  templateUrl: './item-doc-name.html',
  styleUrl: './item-doc-name.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ItemDocName {
  readonly document = input.required<Document>();

  protected getIcon() {
    const type: string = this.document()?.type;
    const icons: { [key: string]: string } = {
      pdf: 'icons/pdf.svg',
      docx: 'icons/word.svg',
      xlsx: 'icons/excel.svg',
    };

    return icons[type] || '';
  }
}
