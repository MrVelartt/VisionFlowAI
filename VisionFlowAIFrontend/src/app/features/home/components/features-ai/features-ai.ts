import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { FeatureAi } from './feature-ai/feature-ai';
import { File, Bot, Sheet, CircleHelp, LucideIconData } from 'lucide-angular';

export interface Feature {
  id: string;
  title: string;
  description: string;
  icon: LucideIconData;
  classBackgroundColor: string;
  classTextColor: string;
}

@Component({
  selector: 'app-features-ai',
  imports: [FeatureAi],
  templateUrl: './features-ai.html',
  styleUrl: './features-ai.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FeaturesAi {
  protected readonly features = signal<Feature[]>([
    {
      id: 'document-understanding',
      title: 'Comprensión de documentos',
      description:
        'OCR y PNL avanzados para extraer y comprender el contenido de cualquier formato de documento',
      icon: File,
      classBackgroundColor: 'bg-blue-100',
      classTextColor: 'text-blue-800',
    },
    {
      id: 'intelligent-automation',
      title: 'Agentes de IA de Automatización',
      description:
        'Agentes inteligentes que aprenden y automatizan procesos empresariales complejos',
      icon: Bot,
      classBackgroundColor: 'bg-purple-100',
      classTextColor: 'text-purple-800',
    },
    {
      id: 'excel-generation',
      title: 'Generación de Excel',
      description:
        'Genere automáticamente informes estructurados en Excel a partir de los documentos procesados',
      icon: Sheet,
      classBackgroundColor: 'bg-green-100',
      classTextColor: 'text-green-800',
    },
    {
      id: 'n8n-workflows',
      title: 'Flujos de trabajo n8n',
      description:
        'Integración perfecta con n8n para la automatización de flujos de trabajo complejos',
      icon: CircleHelp,
      classBackgroundColor: 'bg-orange-100',
      classTextColor: 'text-orange-800',
    },
  ]);
}
