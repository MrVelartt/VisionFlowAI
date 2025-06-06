import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-simple-header',
  imports: [RouterModule],
  templateUrl: './simple-header.html',
  styleUrl: './simple-header.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SimpleHeader {}
