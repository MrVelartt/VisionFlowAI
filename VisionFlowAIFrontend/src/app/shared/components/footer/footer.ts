import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Scroll } from '@core/services';
import { SECTION_FEAUTURES_ID, SECTION_HOW_IT_WORKS_ID } from '@core/contants';

@Component({
  selector: 'app-footer',
  imports: [RouterModule],
  templateUrl: './footer.html',
  styleUrl: './footer.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Footer {
  private readonly scrollService = inject(Scroll);
  protected readonly SECTION_FEAUTURES_ID = SECTION_FEAUTURES_ID;
  protected readonly SECTION_HOW_IT_WORKS_ID = SECTION_HOW_IT_WORKS_ID;

  protected scrollToSection(sectionId: string) {
    this.scrollService.scrollToElement(sectionId);
  }
}
