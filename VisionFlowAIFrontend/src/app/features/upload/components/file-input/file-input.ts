import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { LucideAngularModule, Upload } from 'lucide-angular';

@Component({
  selector: 'app-file-input',
  imports: [ReactiveFormsModule, LucideAngularModule],
  templateUrl: './file-input.html',
  styleUrl: './file-input.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FileInput {
  readonly fileControl = input.required<FormControl>();

  protected readonly iconUpload = Upload;

  protected fileChange(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files && inputElement.files.length > 0) {
      const file = inputElement.files[0];
      this.fileControl().setValue(file);
    } else {
      this.fileControl().setValue(null);
    }
  }
}
