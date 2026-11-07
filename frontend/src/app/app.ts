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

  // AUTENTICACION
  iniciarSesion() {
    if (!this.username || this.username.trim() === '') {
      alert('🪄 Por favor, ingresa tu nombre de explorador.');
      return;
    }
    if (!this.password || this.password.trim() === '') {
      alert('🪄 Por favor, ingresa tu contraseña secreta.');
      return;
    }

    const credenciales = { username: this.username, password: this.password };
    this.ninosService.login(credenciales).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.username); 
        this.usuarioActual.set(res.username);
        this.isLoggedIn.set(true);
        this.cargarNinos();
      },
      error: (err) => alert("Usuario o contraseña incorrectos. Verifica tus datos.")
    });
  }

  registrarse() {
    if (!this.username || this.username.trim() === '') {
      alert('🪄 Debes elegir un nombre de usuario para registrarte.');
      return;
    }
    if (!this.email || this.email.trim() === '') {
      alert('🪄 El correo electrónico es obligatorio.');
      return;
    }

    if (!this.email.includes('@')) {
      alert('🪄 Por favor, ingresa un correo electrónico válido.');
      return;
    }
    if (!this.password || this.password.trim() === '') {
      alert('🪄 Debes crear una contraseña secreta.');
      return;
    }
    if (this.password.length < 6) {
      alert('🪄 Por seguridad, la contraseña debe tener al menos 6 caracteres.');
      return;
    }

    const datos = { username: this.username, password: this.password, email: this.email };
    this.ninosService.registro(datos).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token);
        this.isLoggedIn.set(true);
        this.cargarNinos();
      },
      error: (err) => alert("Error al registrarse. Es posible que este usuario o correo ya exista.")
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


  cargarNinos() {
    this.ninosService.getNinos().subscribe({
      next: (datos) => this.listaNinos.set(datos),
      error: (err) => {
        if(err.status === 401) this.cerrarSesion();
      }
    });
  }

  guardarNino() {

    if (!this.nuevoNino.nombre || this.nuevoNino.nombre.trim() === '') {
      alert('🪄 ¡Ups! Olvidaste escribir el nombre del explorador.');
      return; 
    }
    if (!this.nuevoNino.edad || this.nuevoNino.edad <= 0 || this.nuevoNino.edad > 15) {
      alert('🪄 Por favor, ingresa una edad válida (ej. entre 2 y 12 años).');
      return;
    }
    if (!this.nuevoNino.intereses || this.nuevoNino.intereses.trim() === '') {
      alert('🪄 ¿Qué le gusta al explorador? Escribe algunos intereses para el cuento.');
      return;
    }
    if (!this.nuevoNino.valores || this.nuevoNino.valores.trim() === '') {
      alert('🪄 Escribe al menos un valor (ej. amistad, respeto) para la historia.');
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
        alert("Error al generar el cuento. Por favor, intenta de nuevo.");
      }
    });
  }
}