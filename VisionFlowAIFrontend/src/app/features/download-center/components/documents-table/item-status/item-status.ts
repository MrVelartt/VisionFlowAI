import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { DocumentStatus } from '@core/models';

@Component({
  selector: 'app-item-status',
  imports: [],
  templateUrl: './item-status.html',
  styleUrl: './item-status.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ItemStatus {
  readonly status = input.required<DocumentStatus>();
}
