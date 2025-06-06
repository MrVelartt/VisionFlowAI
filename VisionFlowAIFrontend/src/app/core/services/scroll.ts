import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Scroll {
  constructor() {}

  scrollToElement(elementId: string) {
    const element = document.getElementById(elementId);
    if (!element) return;
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      inline: 'nearest',
    });
  }
}
