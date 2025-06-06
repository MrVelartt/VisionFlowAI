import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { LucideAngularModule } from 'lucide-angular';
import { DocType } from '../../upload';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-doc-types',
  imports: [LucideAngularModule],
  templateUrl: './doc-types.html',
  styleUrl: './doc-types.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DocTypes {
  readonly docTypes = input.required<DocType[]>();
  readonly docTypecontrol = input.required<FormControl>();

  protected docTypeChange(type: string) {
    this.docTypecontrol().setValue(type);
  }
}
