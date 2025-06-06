import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { LucideAngularModule } from 'lucide-angular';
import { Feature } from '../features-ai';

@Component({
  selector: 'app-feature-ai',
  imports: [LucideAngularModule],
  templateUrl: './feature-ai.html',
  styleUrl: './feature-ai.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FeatureAi {
  readonly feature = input.required<Feature>();
}
