import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { LucideAngularModule } from 'lucide-angular';
import { WorkStep } from '../how-it-works';

@Component({
  selector: 'app-step-work',
  imports: [LucideAngularModule],
  templateUrl: './step-work.html',
  styleUrl: './step-work.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StepWork {
  readonly work = input.required<WorkStep>();
  readonly index = input.required<number>();
}
