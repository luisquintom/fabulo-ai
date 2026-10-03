# Usamos una imagen oficial de Node.js (necesaria para Angular)
FROM node:20-alpine

# Creamos la carpeta de trabajo
WORKDIR /app

# Instalamos Angular CLI globalmente dentro del contenedor
RUN npm install -g @angular/cli

# Exponemos el puerto 4200 (el que usa Angular por defecto)
EXPOSE 4200

# El comando que mantendrá encendido el servidor de Angular
CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]