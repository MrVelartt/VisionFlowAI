import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home').then((m) => m.Home),
  },
  {
    path: 'upload',
    loadComponent: () =>
      import('./features/upload/upload').then((m) => m.Upload),
  },
  {
    path: 'download-center',
    loadComponent: () =>
      import('./features/download-center/download-center').then(
        (m) => m.DownloadCenter
      ),
  },
  {
    path: '**',
    redirectTo: '',
    pathMatch: 'full',
  },
];
