import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AgentEndpoint } from '@core/endpoints';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Agent {
  private readonly http = inject(HttpClient);

  constructor() { }

  getAgent1(): Observable<any> {
    return this.http.get<any>(AgentEndpoint.agent1);
  }
}
