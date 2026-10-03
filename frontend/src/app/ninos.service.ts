import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class NinosService {
  private http = inject(HttpClient); 
  private apiUrl = 'http://localhost:8000/api/ninos/'; 

  getNinos() {
    return this.http.get<any[]>(this.apiUrl);
  }

  // NUEVO: Pide al backend que ejecute OpenAI
  generarCuentoIA(ninoId: number) {
    return this.http.post<any>(`${this.apiUrl}${ninoId}/generar_cuento/`, {});
  }
}