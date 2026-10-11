import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class NinosService {
  private http = inject(HttpClient); 
  private apiUrl = 'http://localhost:8000/api/'; 

  login(credenciales: any) {
    return this.http.post<any>(`${this.apiUrl}login/`, credenciales);
  }

  registro(datos: any) {
    return this.http.post<any>(`${this.apiUrl}registro/`, datos);
  }

  private getHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        'Authorization': `Token ${token}`
      })
    };
  }

  getNinos() {
    return this.http.get<any[]>(`${this.apiUrl}ninos/`, this.getHeaders());
  }

  crearNino(datosNino: any) {
    return this.http.post<any>(`${this.apiUrl}ninos/`, datosNino, this.getHeaders());
  }

  generarCuentoIA(ninoId: number) {
    return this.http.post<any>(`${this.apiUrl}ninos/${ninoId}/generar_cuento/`, {}, this.getHeaders());
  }
}