import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-main-banner',
  imports: [RouterModule],
  templateUrl: './main-banner.html',
  styleUrl: './main-banner.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MainBanner {}
