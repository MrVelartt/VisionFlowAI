import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal,
} from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { DocTypes, FileInput } from './components';
import {
  FileText,
  FilePen,
  FileChartLine,
  FileUser,
  Bot,
  LucideAngularModule,
  LucideIconData,
} from 'lucide-angular';
import { FormBuilder, FormGroup, FormsModule, Validators } from '@angular/forms';
import { toFormControl, touchControlsForm } from '@shared/utils';
import { FormError, SimpleHeader } from '@shared/components';

export interface DocType {
  type: string;
  name: string;
  icon: LucideIconData;
}

@Component({
  selector: 'app-upload',
  imports: [
    RouterModule,
    DocTypes,
    FileInput,
    FormsModule,
    LucideAngularModule,
    SimpleHeader,
    FormError
  ],
  templateUrl: './upload.html',
  styleUrl: './upload.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Upload {
  private readonly formBuilder = inject(FormBuilder);
  private readonly router = inject(Router);

  protected readonly form = signal<FormGroup>(this.createForm());
  protected readonly docTypes = signal<DocType[]>([
    {
      type: 'inovice',
      name: 'Factura',
      icon: FileUser,
    },
    {
      type: 'quote',
      name: 'Cotización',
      icon: FileChartLine,
    },
    {
      type: 'blueprint',
      name: 'Planos',
      icon: FilePen,
    },
    {
      type: 'other',
      name: 'Otro',
      icon: FileText,
    },
  ]);
  protected readonly toFormControl = toFormControl;
  protected readonly iconBot = Bot;

  protected onSubmit(): void {
    // this.router.navigate(['download-center']);
    console.log('Navigating to download center');
    const form = this.form();
    if (form.invalid) {
      touchControlsForm(form);
      return;
    }

    console.log('Form submitted:', form.value);
  }

  private createForm(): FormGroup {
    return this.formBuilder.group({
      file: [null, Validators.required],
      docType: [null, Validators.required],
    });
  }
}
