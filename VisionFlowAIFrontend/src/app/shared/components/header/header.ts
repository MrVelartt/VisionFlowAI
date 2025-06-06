import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal,
} from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import {
  SECTION_FEAUTURES_ID,
  SECTION_HOME_ID,
  SECTION_HOW_IT_WORKS_ID,
} from '@core/contants';
import { NavItem } from '@core/models';
import { Scroll } from '@core/services';

@Component({
  selector: 'app-header',
  imports: [RouterModule],
  templateUrl: './header.html',
  styleUrl: './header.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Header {
  private readonly scrollService = inject(Scroll);
  private readonly router = inject(Router);

  protected readonly navItems = signal<NavItem[]>([
    { id: 'home', label: 'Inicio', sectionId: SECTION_HOME_ID },
    {
      id: 'features',
      label: 'Características',
      sectionId: SECTION_FEAUTURES_ID,
    },
    {
      id: 'how-it-works',
      label: 'Cómo funciona',
      sectionId: SECTION_HOW_IT_WORKS_ID,
    },
    { id: 'upload-file', label: 'Cargar documento', route: '/upload' },
    { id: 'download', label: 'Descargas', route: '/download-center' },
  ]);

  protected readonly showMenuMobile = signal(false);

  constructor() {}

  protected clickNavItem(item: NavItem) {
    if (item.sectionId) {
      this.scrollToSection(item.sectionId);
      return;
    }

    this.router.navigate([item.route || '/']);
  }

  protected scrollToSection(sectionId: string) {
    this.scrollService.scrollToElement(sectionId);
  }

  protected toggleMenuMobile() {
    this.showMenuMobile.update((prev) => !prev);
  }
}
