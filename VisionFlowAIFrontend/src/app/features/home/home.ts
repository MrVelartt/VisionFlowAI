import { ChangeDetectionStrategy, Component } from '@angular/core';
import { HowItWorks, MainBanner } from './components';
import { FeaturesAi } from './components/features-ai/features-ai';
import { Footer, Header } from '@shared/components';

@Component({
  selector: 'app-home',
  imports: [Header, Footer, MainBanner, FeaturesAi, HowItWorks],
  templateUrl: './home.html',
  styleUrl: './home.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Home {}
