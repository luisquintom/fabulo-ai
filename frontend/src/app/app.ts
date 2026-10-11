import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { NinosService } from './ninos.service'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {

  isLoggedIn = signal<boolean>(false);
  usuarioActual = signal<string>('');
  mostrarRegistro = signal<boolean>(false); 
  
  username = '';
  password = '';
  email = '';

  listaNinos = signal<any[]>([]); 
  cuentoGenerado = signal<any>(null); 
  cargando = signal<boolean>(false);  
  
  mostrarFormularioNino = signal<boolean>(false);
  nuevoNino = { nombre: '', edad: null as number | null, intereses: '', valores: '' };

  private ninosService = inject(NinosService); 

  ngOnInit() {
    if (localStorage.getItem('token')) {
      this.isLoggedIn.set(true);
      this.usuarioActual.set(localStorage.getItem('username') || '');
      this.cargarNinos();
    }
  }

  // --- MET AUTENTICACIÓN ---
  iniciarSesion() {
    const credenciales = { username: this.username, password: this.password };
    this.ninosService.login(credenciales).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.username); 
        this.usuarioActual.set(res.username);
        this.isLoggedIn.set(true);
        this.cargarNinos();
      },
      error: (err) => alert("Usuario o contraseña incorrectos")
    });
  }

  registrarse() {
    const datos = { username: this.username, password: this.password, email: this.email };
    this.ninosService.registro(datos).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token);
        this.isLoggedIn.set(true);
        this.cargarNinos();
      },
      error: (err) => alert("Error al registrarse. El usuario podría ya existir.")
    });
  }

  cerrarSesion() {
    localStorage.removeItem('token');
    localStorage.removeItem('username'); 
    this.usuarioActual.set('');
    this.isLoggedIn.set(false);
    this.listaNinos.set([]);
    this.cuentoGenerado.set(null);
    this.username = '';
    this.password = '';
  }

  // --- MET DEL PANEL ---
  cargarNinos() {
    this.ninosService.getNinos().subscribe({
      next: (datos) => this.listaNinos.set(datos),
      error: (err) => {
        if(err.status === 401) this.cerrarSesion();
      }
    });
  }

  guardarNino() {
    if (!this.nuevoNino.nombre || !this.nuevoNino.edad) {
      alert("Por favor, completa al menos el nombre y la edad.");
      return;
    }

    this.ninosService.crearNino(this.nuevoNino).subscribe({
      next: (res) => {
        this.cargarNinos(); 
        this.mostrarFormularioNino.set(false); 
        this.nuevoNino = { nombre: '', edad: null, intereses: '', valores: '' }; 
      },
      error: (err) => alert("Error al guardar el perfil del niño.")
    });
  }

  pedirCuento(ninoId: number) {
    this.cargando.set(true);
    this.cuentoGenerado.set(null); 
    
    this.ninosService.generarCuentoIA(ninoId).subscribe({
      next: (cuento) => {
        this.cuentoGenerado.set(cuento);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error(err);
        this.cargando.set(false);
        alert("Error al generar el cuento.");
      }
    });
  }
}