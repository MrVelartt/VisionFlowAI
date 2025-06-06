import { AbstractControl, FormControl, FormGroup } from '@angular/forms';

export const toFormControl = (control: AbstractControl | null): FormControl => {
  return control as FormControl;
};

/** Función estatica que recibe por parametro el formulario al cual se le aplicaran las validaciones*/
export const touchControlsForm = (form: FormGroup): void => {
  Object.keys(form.controls).forEach((k) => {
    form.get(k)?.markAsTouched();
    form.get(k)?.markAsDirty();
    form.get(k)?.markAsPristine();
    form.get(k)?.updateValueAndValidity({ emitEvent: true });
  });
};
