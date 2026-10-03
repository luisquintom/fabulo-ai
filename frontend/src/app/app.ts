import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NinosService } from './ninos.service'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  listaNinos = signal<any[]>([]); 
  cuentoGenerado = signal<any>(null); // Guardará el cuento cuando OpenAI responda
  cargando = signal<boolean>(false);  // Bloqueará botones mientras carga
  
  private ninosService = inject(NinosService); 

  ngOnInit() {
    this.ninosService.getNinos().subscribe(datos => this.listaNinos.set(datos));
  }

  // Función que se activa al hacer clic en el botón
  pedirCuento(ninoId: number) {
    this.cargando.set(true);
    this.cuentoGenerado.set(null); // Limpiamos la pantalla por si había un cuento anterior
    
    this.ninosService.generarCuentoIA(ninoId).subscribe({
      next: (cuento) => {
        this.cuentoGenerado.set(cuento);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error(err);
        this.cargando.set(false);
        alert("Error al generar el cuento. Revisa la consola o tu API Key.");
      }
    });
  }
}