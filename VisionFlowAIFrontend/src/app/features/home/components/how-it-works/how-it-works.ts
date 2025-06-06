import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { StepWork } from './step-work/step-work';
import { Upload, Brain, FileDown, CalendarCog, LucideIconData } from 'lucide-angular';

export interface WorkStep {
  id: string;
  title: string;
  description: string;
  icon: LucideIconData;
  classBackgroundColor: string;
  classTextColor: string;
}

@Component({
  selector: 'app-how-it-works',
  imports: [StepWork],
  templateUrl: './how-it-works.html',
  styleUrl: './how-it-works.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HowItWorks {
  protected readonly works = signal<WorkStep[]>([
    {
      id: 'upload-documents',
      title: 'Cargar documentos',
      description:
        'Arrastre y suelte o cargue sus documentos empresariales en cualquier formato',
      icon: Upload,
      classBackgroundColor: 'bg-blue-800',
      classTextColor: 'text-blue-800',
    },
    {
      id: 'ai-processing',
      title: 'Procesamiento con IA',
      description:
        'Nuestra IA analiza y extrae información clave mediante visión por ordenador',
      icon: Brain,
      classBackgroundColor: 'bg-purple-800',
      classTextColor: 'text-purple-800',
    },
    {
      id: 'generate-excel',
      title: 'Generación de Excel',
      description:
        'Obtenga datos estructurados exportados a Excel con información organizada',
      icon: FileDown,
      classBackgroundColor: 'bg-green-800',
      classTextColor: 'text-green-800',
    },
    {
      id: 'schedule-workflows',
      title: 'Automatización de tareas',
      description:
        'Active flujos de trabajo automatizados e intégrelos con sus sistemas actuales',
      icon: CalendarCog,
      classBackgroundColor: 'bg-orange-800',
      classTextColor: 'text-orange-800',
    },
  ]);
}
