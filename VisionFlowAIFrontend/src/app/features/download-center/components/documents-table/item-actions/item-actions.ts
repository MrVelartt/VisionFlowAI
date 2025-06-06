import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { DocumentStatus } from '@core/models';
import {
  FileDown,
  LucideAngularModule,
  Eye,
  RotateCcw,
  Clock,
} from 'lucide-angular';

@Component({
  selector: 'app-item-actions',
  imports: [LucideAngularModule],
  templateUrl: './item-actions.html',
  styleUrl: './item-actions.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ItemActions {
  readonly status = input.required<DocumentStatus>();
  readonly downloadChange = output<void>();
  readonly viewChange = output<void>();
  readonly retryChange = output<void>();

  protected readonly iconFileDowm = FileDown;
  protected readonly iconEye = Eye;
  protected readonly iconRotateCcw = RotateCcw;
  protected readonly iconClock = Clock;

  protected onDownload(): void {
    this.downloadChange.emit();
  }

  protected onView(): void {
    this.viewChange.emit();
  }

  protected onRetry(): void {
    this.retryChange.emit();
  }
}
